import pika
import os

# create a directory for storing the tweets
os.makedirs('tweets', exist_ok=True)

# define the callback function to handle incoming messages
def callback(ch, method, properties, body):
    tweet = body.decode()
    # save the tweet as a file in the tweets directory
    with open(f'tweets/{method.delivery_tag}.txt', 'w') as f:
        f.write(tweet)
    # acknowledge that the message has been received and processed
    ch.basic_ack(delivery_tag=method.delivery_tag)

# connect to the RabbitMQ server and start consuming tweets from the queue
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='tweets', durable=True)
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='tweets', on_message_callback=callback)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
