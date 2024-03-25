import uuid
import grpc
from concurrent import futures
import market_pb2
import market_pb2_grpc
import time
from concurrent import futures

_ONE_DAY_IN_SECONDS = 60 * 60 * 24
counter = 1

class MarketClient:
    def __init__(self, server_address):
        self.channel = grpc.insecure_channel(server_address)
        self.stub = market_pb2_grpc.NotificationServiceStub(self.channel)

    def notify(self, message):
        request = market_pb2.Notification(message=message)
        # response = self.stub.send_notification(request)
        response = self.stub.NotifyClient(request)
        print(f"Notification Response: {response.acknowledged}")

class MarketServicer(market_pb2_grpc.MarketServicer):
    def __init__(self):
        self.sellers = {}  # Dictionary to store seller information
        self.items_for_sale = {}  # Dictionary to store items for sale
        self.wishlists = {}  # Dictionary to store buyer wishlists
        self.buyer_streams = {} # Dictionary to keep track of buyers
        self.items_with_sellers = {}    # Dictionary to map seller to an item ID
        self.ratings = {}   # Dictionary to store the ratings of products and by which buyer was the rating recorded

    def RegisterSeller(self, request, context):
        address = request.address
        uuid_str = request.uuid

        if uuid_str in self.sellers.values():
            return market_pb2.SuccessResponse(success=False)

        self.sellers[address] = uuid_str
        print(f"Seller join request from {address}, uuid = {uuid_str}")
        return market_pb2.SuccessResponse(success=True)

    def RegisterBuyer(self, request, context):
        buyer_address = context.peer().split(":")[0]
        self.add_buyer_stream(buyer_address, context)
        return market_pb2.SuccessResponse(success=True)

    def add_buyer_stream(self, buyer_address, context):
        self.buyer_streams[buyer_address] = context

    def SellItem(self, request, context):
        global counter
        seller_address = request.seller_info.address
        seller_uuid = request.seller_info.uuid

        # item_id = len(self.items_for_sale) + 1  #rejected due to the delete item option potentially creating duplicate item IDs        
        item_id = str(counter)
        rating = float(5)
        item_details = {
            'item_id': item_id,
            'name': request.name,
            'category': request.category,
            'quantity': request.quantity,
            'description': request.description,
            'seller_info': request.seller_info,
            'price_per_unit': request.price_per_unit,
            'rating': rating
        }
        self.items_for_sale[item_id] = item_details
        self.items_with_sellers[counter] = seller_address
        counter += 1
        print(f"Sell Item request from {seller_address}")
        return market_pb2.SuccessResponse(success=True)

    def UpdateItem(self, request, context):
        item_id = request.item_id.item_id
        seller_address = request.seller_info.address
        seller_uuid = request.seller_info.uuid

        if seller_address not in self.sellers or self.sellers[seller_address] != seller_uuid:
            return market_pb2.SuccessResponse(success=False)

        if item_id not in self.items_for_sale:
            return market_pb2.SuccessResponse(success=False)

        updated_item = self.items_for_sale[item_id]
        updated_item['price_per_unit'] = request.new_price
        updated_item['quantity'] = request.new_quantity

        print(f"Update Item {item_id} request from {seller_address}")
        # for item in self.wishlists.keys():
        #     if item_id == item:
        #         address_buyers_wishlisted = self.wishlists[item]
        #         for i in address_buyers_wishlisted:
        #             market_client = MarketClient(i)
        #             message = f"A product on your wishlist has recently been updated.\nThe new details are:\n{updated_item}"
        #             market_client.notify(message)
        #         break

        return market_pb2.SuccessResponse(success=True)

    def DeleteItem(self, request, context):
        item_id = request.item_id.item_id
        seller_address = request.seller_info.address
        seller_uuid = request.seller_info.uuid

        if seller_address not in self.sellers or self.sellers[seller_address] != seller_uuid:
            return market_pb2.SuccessResponse(success=False)

        if item_id in self.items_for_sale:
            del self.items_for_sale[item_id]
            del self.items_with_sellers[int(item_id)]
            print(f"Delete Item {item_id} request from {seller_address}")
            return market_pb2.SuccessResponse(success=True)

        return market_pb2.SuccessResponse(success=False)

    def DisplaySellerItems(self, request, context):
        seller_address = request.address
        seller_uuid = request.uuid
        # if seller_address in self.sellers.values() and self.sellers[seller_address] == seller_address:
        if seller_address in self.sellers.keys() and seller_address in self.items_with_sellers.values():
            items = self.items_for_sale.values()
            display_items = market_pb2.DisplayItems(items=[market_pb2.ItemDetails(
                item_id=market_pb2.ItemID(item_id=item['item_id']),
                name=item['name'],
                category=item['category'],
                quantity=int(item['quantity']),
                description=item['description'],
                seller_info=item['seller_info'],
                price_per_unit=item['price_per_unit'],
                rating=item['rating']
            ) for item in items if item['seller_info'].uuid==seller_uuid])
            print(f"Display Items request from {seller_address}")
            return display_items

        return market_pb2.DisplayItems(items=[])

    def SearchItem(self, request, context):
        item_name = request.item_name
        category = request.category

        filtered_items = [item for item in self.items_for_sale.values()
                          if (not item_name or item['name'] == item_name) and
                        #   (category == market_pb2.SearchRequest."ANY" or item['category'] == category)]
                        (category == "ANY" or item["category"]==category)]

        display_items = market_pb2.DisplayItems(items=[market_pb2.ItemDetails(
            item_id=market_pb2.ItemID(item_id=item['item_id']),
            name=item['name'],
            category=item['category'],
            quantity=item['quantity'],
            description=item['description'],
            seller_info=item['seller_info'],
            price_per_unit=item['price_per_unit'],
            rating=item['rating']
        ) for item in filtered_items])

        print(f"Search request for Item: {item_name}, Category: {category}.")
        return display_items

    def BuyItem(self, request, context):
        item_id = request.item_id.item_id
        quantity = request.quantity
        buyer_address = request.buyer_info.address

        if item_id in self.items_for_sale.keys() and self.items_for_sale[item_id]['quantity'] >= quantity:
            self.items_for_sale[item_id]['quantity'] -= quantity
            print(f"Buy request {quantity} of item {item_id}, from {buyer_address}")
            market_client = MarketClient(self.items_with_sellers[int(item_id)])
            message = f"{quantity} units of item {item_id}: {self.items_for_sale[item_id]['name']} has been purchased by a customer."
            # market_client.notify(message)
            if self.items_for_sale[item_id]['quantity'] == 0:
                del self.items_for_sale[item_id]
                del self.items_with_sellers[int(item_id)]
            return market_pb2.SuccessResponse(success=True)

        return market_pb2.SuccessResponse(success=False)

    def AddToWishList(self, request, context):
        item_id = request.item_id.item_id
        buyer_address = request.buyer_info.address
        buyer_uuid = request.buyer_info.uuid

        if item_id in self.items_for_sale:
            if item_id not in self.wishlists.keys():
                self.wishlists[item_id] = set()

            self.wishlists[item_id].add(buyer_address)
            print(f"Wishlist request of item {item_id}, from {buyer_address}")
            return market_pb2.SuccessResponse(success=True)

        return market_pb2.SuccessResponse(success=False)

    def RateItem(self, request, context):
        item_id = request.item_id.item_id
        buyer_address = request.buyer_info.address
        buyer_uuid = request.buyer_info.uuid
        rating = request.rating

        if item_id in self.items_for_sale and 0 <= rating <= 5:
            if item_id not in self.ratings: # The item has never been rated before. (Default rating = 5 by the seller.)
                self.ratings[item_id] = {'total':rating, 'count':1, 'buyer_uuid':[request.buyer_uuid]}

            else:
                for item_id in self.ratings:
                    if buyer_uuid in self.ratings[item_id]['buyer_uuid']:
                        print(f"The buyer was not permitted to rate this item again.")
                        return market_pb2.SuccessResponse(success=False)
                self.ratings[item_id]['total'] += rating
                self.ratings[item_id]['count'] += 1
                self.ratings[item_id]['buyer_uuid'].append(buyer_uuid)
            average_rating = self.ratings[item_id]['total']/self.ratings[item_id]['count']
            self.items_for_sale[item_id]['rating'] = average_rating
            print(f"{buyer_address} rated item {item_id} with {rating} stars. The updated average rating: {average_rating}.")
            return market_pb2.SuccessResponse(success=True)

        return market_pb2.SuccessResponse(success=False)

def serve():
    port = '50051'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    servicer = MarketServicer()
    market_pb2_grpc.add_MarketServicer_to_server(servicer, server)
    server.add_insecure_port('[::]:'+port)
    server.start()
    print(f"Welcome to the market!")
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)
    # server.wait_for_termination()

if __name__ == '__main__':
    serve()
