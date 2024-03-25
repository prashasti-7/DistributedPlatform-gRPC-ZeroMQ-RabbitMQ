import pika
import sys
import json

class Youtuber:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

        # self.credentials =pika.PlainCredentials('shruti', 'shruti')
        # self.connection =pika.BlockingConnection(pika.ConnectionParameters('34.41.221.73', credentials=self.credentials))

        self.channel = self.connection.channel()

        self.channel.queue_declare(queue='ack_queue', durable=True)  # Declaring the acknowledgment queue
        self.channel.basic_consume(queue='ack_queue', on_message_callback=self.callback_ack, auto_ack=True)  # Setting up a consumer for the acknowledgment queue

    def callback_ack(self, ch, method, properties, body):
        print("SUCCESS: Video received by YouTube Server")
        sys.exit(0)  # Exit the program after receiving acknowledgment

    def publish_video(self, youtuber_name, video_name):
        message = {
            "type": "youtuber",
            "action": "UPLOAD",
            "youtuber_name": youtuber_name,
            "video_name": video_name
        }
        self.channel.basic_publish(exchange='youtuber_requests', routing_key='', body=json.dumps(message))
        print("Video sent to YouTube Server")

if __name__ == "__main__":
    youtuber_client = Youtuber()

    if len(sys.argv) < 3:
        print("Usage: python Youtuber.py <YoutuberName> <VideoName>")
        sys.exit(1)

    youtuber_name = sys.argv[1]
    video_name = ' '.join(sys.argv[2:])  # Join all arguments starting from index 2 with space

    youtuber_client.publish_video(youtuber_name, video_name)

    # Start consuming messages to receive acknowledgment
    print('Waiting for acknowledgment...')
    youtuber_client.channel.start_consuming()