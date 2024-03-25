import pika
import json
import sys

class YoutubeServer:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        
        self.channel.exchange_declare(exchange='video_notifications', exchange_type='fanout')
        
        self.youtubers = {}
        self.users = {}
        self.youtuber_user = {}

    def consume_requests(self):
        result = self.channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue
        
        self.channel.queue_bind(exchange='user_requests', queue=queue_name)
        self.channel.queue_bind(exchange='youtuber_requests', queue=queue_name)

        def callback(ch, method, properties, body):
            message = json.loads(body.decode())
            if message['type'] == 'user':
                self.handle_user_request(message)
            elif message['type'] == 'youtuber':
                self.handle_youtuber_request(message)

        self.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
        print("Consuming Requests...")
        self.channel.start_consuming()

    def handle_user_request(self, message):
        user_name = message['user']
        if user_name not in self.users:
            self.users[user_name] = User(user_name)
            user_queue_name = f'queue_{user_name}'
            self.channel.queue_declare(queue=user_queue_name)

        user = self.users[user_name]
        youtuber_name = message.get('youtuber')  # Optional field for YouTuber's name
        subscribe = message.get('subscribe')  # Optional field for subscription action

        if subscribe is not None and youtuber_name is not None: #this is to handle the subscription part of the youtuber
            if youtuber_name not in self.youtubers:
                print(f"{youtuber_name} does not exist, please enter a valid youtuber")
                sys.exit(0)
            if subscribe == "True":
                user.add_subscription(youtuber_name)
                self.youtuber_user[youtuber_name].add(user_name)
            elif subscribe == "False":
                if youtuber_name in user.subscriptions:
                    user.subscriptions.remove(youtuber_name)
                    self.youtuber_user[youtuber_name].remove(user_name)
            
        user_queue_name = f'queue_{user_name}'
        acknowledgment_message = { "acknowledgement": "Request received by YouTube Server",
                                  "subscription_status": f"{user_name} {'subscribed' if subscribe == 'True' else 'unsubscribed'} to {youtuber_name}"}
        self.channel.basic_publish(exchange='', routing_key=user_queue_name, body=json.dumps(acknowledgment_message))
        print("Acknowledgment sent to User")

    def handle_youtuber_request(self, message): #done
        youtuber_name = message['youtuber_name']
        video_name = message['video_name']
        
        if youtuber_name not in self.youtubers:
            self.youtubers[youtuber_name] = Youtuber(youtuber_name)  #this is to add a new youtuber (uses the youtuber class)
            self.youtuber_user[youtuber_name] = set()
        self.youtubers[youtuber_name].add_video(video_name) #adds the video of the youtuber in the set of the youtuber
        self.send_notification(youtuber_name, video_name) #the idea is to add the notifications in the user's queue #can think of some other method too

        acknowledgment_message = { "message": "Video received by YouTube Server"} 
        self.channel.basic_publish(exchange='', routing_key='ack_queue', body=json.dumps(acknowledgment_message))
        print("Acknowledgment sent to Youtuber")

    def send_notification(self, youtuber_name, video_name):  
        subscribers = self.youtuber_user.get(youtuber_name, set())
        for subscriber in subscribers:
            user_queue_name = f'queue_{subscriber}'
            message = {"notification": f'{youtuber_name} uploaded the video {video_name}'}
            self.channel.basic_publish(exchange='', routing_key=user_queue_name, body=json.dumps(message))
            print(f"Video published to {subscriber}'s queue: {video_name}")

class User:
    def __init__(self, user_name):
        self.user_name = user_name
        self.subscriptions = set()

    def add_subscription(self, youtuber_name):
        self.subscriptions.add(youtuber_name)

class Youtuber:
    def __init__(self, youtuber_name):
        self.youtuber_name = youtuber_name
        self.videos = set()

    def add_video(self, video_name):
        self.videos.add(video_name)

if __name__ == "__main__":
    server = YoutubeServer()
    server.consume_requests()