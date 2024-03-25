import pika
import sys
import json

class User:
    def __init__(self, user_name):
        self.user_name = user_name
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

        # self.credentials =pika.PlainCredentials('shruti', 'shruti')
        # self.connection =pika.BlockingConnection(pika.ConnectionParameters('34.41.221.73', credentials=self.credentials))

        self.channel = self.connection.channel()
        
        # self.channel.queue_declare(queue='ack_queue', durable=True)  # Declaring the acknowledgment queue
        # self.channel.basic_consume(queue='ack_queue', on_message_callback=self.callback_ack, auto_ack=True)  # Setting up a consumer for the acknowledgment queue

        self.user_queue_name = f'queue_{self.user_name}' # Declare the user's queue
        self.channel.queue_declare(queue=self.user_queue_name)
        self.channel.basic_consume(queue=self.user_queue_name, on_message_callback=self.receive_notifications, auto_ack=True)
        self.response = None

    # def callback_ack(self, ch, method, properties, body):
    #     print(body)
    #     print("SUCCESS: Logged in successfully")
    #     self.start_consuming_user_queue()  # Start consuming notifications after logging in

    def login(self):
        message = {
            "type": "user",
            "user": self.user_name,
            "action": "login"
        }
        self.channel.basic_publish(exchange='user_requests', routing_key='', body=json.dumps(message))
        print("Request Sent to YouTube Server")

    def update_subscription(self, youtuber_name, action):
        subscribe = "True" if action == 's' else "False"  
        message = {
            "type": "user",
            "user": self.user_name,
            "youtuber": youtuber_name,
            "subscribe": subscribe
        }
        self.channel.basic_publish(exchange='user_requests', routing_key='', body=json.dumps(message))
        print("Request Sent to YouTube Server")

    def receive_notifications(self, channel, method, properties, body):
        message = json.loads(body.decode())
        print(message)
        sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 4:
        print("Usage: python User.py <UserName> <Action: s/u> [<YouTuberName>]")
        sys.exit(1)

    user_name = sys.argv[1]
    user = User(user_name)

    if len(sys.argv) == 2:
        user.login()
    elif len(sys.argv) == 4:
        action = sys.argv[2]
        youtuber_name = sys.argv[3]
        user.update_subscription(youtuber_name, action)

    print('Waiting for acknowledgment...') # Start consuming messages to receive acknowledgment
    user.channel.start_consuming()