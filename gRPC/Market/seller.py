import grpc
import market_pb2
import market_pb2_grpc
import uuid
from concurrent import futures
import threading

def seller_notif_server():
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        market_pb2_grpc.add_NotificationServiceServicer_to_server(SellerNotificationServicer(), server)
        server.add_insecure_port('localhost:50056')
        server.start()
        print("Server Notification: Server Started")
        server.wait_for_termination()

class SellerNotificationServicer(market_pb2_grpc.NotificationService):
    def send_notification(self, request, context):
        print(f"Notification received by the seller: {request.message}")
        return market_pb2.NotifyResponse(message="Notification received")


class SellerClient:
    def __init__(self):
        self.address = 'localhost:50051'
        self.channel = grpc.insecure_channel(self.address)
        self.stub = market_pb2_grpc.MarketStub(self.channel)

    def register_seller(self, seller_uuid):
        # request = market_pb2.SellerInfo(address=seller_address, uuid=self.uuid)
        seller_address = self.address
        request = market_pb2.SellerInfo(address=seller_address, uuid=seller_uuid)
        response = self.stub.RegisterSeller(request)
        return response.success

    def sell_item(self, name, category, quantity, description, seller_uuid, price_per_unit):
        seller_address = self.address
        item_details = market_pb2.ItemDetails(
            # item_id=market_pb2.ItemID(item_id=item_id),
            name=name,
            category=category,
            quantity=quantity,
            description=description,
            seller_info=market_pb2.SellerInfo(address=seller_address, uuid=seller_uuid),
            price_per_unit=price_per_unit
        )
        response = self.stub.SellItem(item_details)
        return response.success

    def update_item(self, item_id, new_price, new_quantity, seller_uuid):
        seller_address = self.address
        request = market_pb2.UpdateItemRequest(
            item_id=market_pb2.ItemID(item_id=item_id),
            new_price=new_price,
            new_quantity=new_quantity,
            seller_info=market_pb2.SellerInfo(address=seller_address, uuid=seller_uuid)
        )
        response = self.stub.UpdateItem(request)
        return response.success

    def delete_item(self, item_id, seller_uuid):
        seller_address = self.address
        request = market_pb2.DeleteItemRequest(
            item_id=market_pb2.ItemID(item_id=item_id),
            seller_info=market_pb2.SellerInfo(address=seller_address, uuid=seller_uuid)
        )
        response = self.stub.DeleteItem(request)
        return response.success

    def display_seller_items(self, seller_uuid):
        seller_address = self.address
        request = market_pb2.SellerInfo(address=seller_address, uuid=seller_uuid)
        response = self.stub.DisplaySellerItems(request)
        return response.items

if __name__ == "__main__":
    print("Welcome!")
    # server_notif_thread = threading.Thread(target=seller_notif_server)
    # server_notif_thread.start()
    seller_client = 0
    print("Seller Menu")
    while True:
        print("The following options are available for you as a seller: ")
        print("1. Register as a seller\n2. Add an item to your list\n3. Update the details of an item\n4. Delete an item from your list\n5. Display all your items\n6. Exit ")
        ch = int(input("Enter choice: "))
        if ch==6:
            break
        elif ch==1:
            seller_client = SellerClient()
            seller_uuid = str(uuid.uuid1())
            res = seller_client.register_seller(seller_uuid)
            if res:
                print("SUCCESS")
                print(f"You have been registered successfully as a seller in the marketplace with the ID {seller_uuid}\nPlease note the UUID which will be used for authentication.")
            else:
                print("FAILURE!")
                print(f"You have already been registered as a seller.")
        elif seller_client==0:
            print(f"You have to register as a seller to avail the functionalities of this marketplace. Sorry, try again!")
        elif ch==2:
            item_name = input("Enter the name of the item: ")
            item_category = int(input("Enter the category of the item:\n1. Electronics\n2. Fashion\n3. Others\n"))
            if item_category == 1:
                category = "ELECTRONICS"
            elif item_category == 2:
                category = "FASHION"
            else:
                category = "OTHERS"
            item_quantity = int(input("Enter the quantity in which the item is available: "))
            item_price = int(input(f"Enter the price of one unit of {item_name}: "))
            item_desc = input("Enter the description of the item: ")
            res = seller_client.sell_item(item_name, category, item_quantity, item_desc, seller_uuid, item_price)
            print(res)

        elif ch==3:
            item_id = input("Enter item ID of the product you want to update: ")
            item_price = int(input("Enter new price of the item: "))
            item_quantity = int(input("Enter the quantity of the product available: "))
            res = seller_client.update_item(item_id, item_price, item_quantity, seller_uuid)
            print(res)

        elif ch==4:
            item_id = input("Enter item ID of the product you want to remove: ")
            res = seller_client.delete_item(item_id, seller_uuid)

        elif ch==5:
            res = seller_client.display_seller_items(seller_uuid)
            n_items = len(res)
            if n_items==0:
                print(f"You have not added any items currently.")
            else:
                for item in res:
                    print(item)

        else:
            break
    print("Thankyou!")
