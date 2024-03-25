import grpc
import market_pb2
import market_pb2_grpc
import uuid
from concurrent import futures
import time
import threading

def buyer_notif_server():
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        market_pb2_grpc.add_NotificationServiceServicer_to_server(BuyerNotificationServicer(), server)
        server.add_insecure_port('localhost:50056')
        server.start()
        print("Server Notification: Server Started")
        server.wait_for_termination()

class BuyerNotificationServicer(market_pb2_grpc.NotificationServiceServicer):
    def send_notification(self, request, context):
        print(f"Notification received by the buyer: {request.message}")
        return market_pb2.NotifyResponse(message="Notification received")

class BuyerClient:
    def __init__(self):
        self.address = 'localhost:50051'
        self.channel = grpc.insecure_channel(self.address)
        self.stub = market_pb2_grpc.MarketStub(self.channel)
        self.uuid = str(uuid.uuid1())

    def search_item(self, item_name, category="ANY"):
        request = market_pb2.SearchRequest(item_name=item_name, category=category)
        response = self.stub.SearchItem(request)
        return response.items

    def buy_item(self, item_id, quantity, buyer_uuid):
        buyer_address = self.address
        request = market_pb2.BuyRequest(
            item_id=market_pb2.ItemID(item_id=item_id),
            quantity=quantity,
            buyer_info=market_pb2.BuyerInfo(address=buyer_address, uuid=buyer_uuid)
        )
        response = self.stub.BuyItem(request)
        if response.success:
            print(f"SUCCESS!")
            print("You have purchased the item successfully!")
        else:
            print(f"FAILURE!")
            print(f"The item is not available in the marketplace in the quantity your require.")
        # return response.success

    def add_to_wishlist(self, item_id, buyer_uuid):
        buyer_address = self.address
        request = market_pb2.AddToWishListRequest(
            item_id=market_pb2.ItemID(item_id=item_id),
            buyer_info=market_pb2.BuyerInfo(address=buyer_address, uuid=buyer_uuid)
        )
        response = self.stub.AddToWishList(request)
        return response.success

    def rate_item(self, item_id, buyer_uuid, rating):
        buyer_address = self.address
        request = market_pb2.RateItemRequest(
            item_id=market_pb2.ItemID(item_id=item_id),
            buyer_info=market_pb2.BuyerInfo(address=buyer_address, uuid=buyer_uuid),
            rating=rating
        )
        response = self.stub.RateItem(request)
        return response.success

if __name__ == "__main__":
    buyer_client = BuyerClient()
    print("Welcome!")
    
    # buyer_notif_thread = threading.Thread(target=buyer_notif_server)
    # buyer_notif_thread.start()

    buyer_uuid = str(uuid.uuid1())
    print(f"Your Buyer UUID is {buyer_uuid}")
    print("The following options are available for you as a customer: ")
    while True:
        print("1. Search for an item\n2. Buy an item\n3. Add an item to your wishlist\n4. Rate an item in the marketplace\n5. Exit ")
        ch = int(input("Enter choice: "))

        if ch==5:
            break

        elif ch==1:
            item_name = input("Enter the name of the item you are looking for: ")
            item_category = int(input("Enter the category of the item you're looking for:\n1.Electronics\n2.Fashion\n3.Others\n4.Any (Show all items): "))
            if item_category==1:
                category = "ELECTRONICS"
            elif item_category==2:
                category = "FASHION"
            elif item_category==3:
                category = "OTHERS"
            else:
                category = "ANY"
            res = buyer_client.search_item(item_name, category)
            print(res)

        elif ch==2:
            item_id = input("Enter the item ID of the product you want to purchase: ")
            item_quantity = int(input("Enter the quantity in which you want to purchase this item: "))
            res = buyer_client.buy_item(item_id, item_quantity, buyer_uuid)
            print(res)
        
        elif ch==3:
            item_id = input("Enter the item ID of the product you want to add to your wishlist: ")
            res = buyer_client.add_to_wishlist(item_id, buyer_uuid)
            if res:
                print("SUCCESS!")
            else:
                print("FAILURE!")

        elif ch==4:
            item_id = input("Enter the item ID of the product you want to rate: ")
            rating = float(int(input("Enter a rating (an integer from 0 to 5): ")))
            res = buyer_client.rate_item(item_id, buyer_uuid, rating)
            if res:
                print("SUCCESS!")
            else:
                print("FAILURE!")
        else:
            ch = int(input("Are you sure you want to exit? Enter 1 to go back to menu or 0 to exit: "))
            if ch == 1:
                continue
            else:
                break
    print("Thankyou for shopping!")
