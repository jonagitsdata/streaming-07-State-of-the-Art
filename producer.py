import pika
import csv

# define send_tweet function to queue
def send_tweet(host: str, queue_name: str, tweet: str):
    """
    Creates and sends a tweet to the queue each execution.

    Parameters:
        host (str): the host name or IP address of the RabbitMQ server
        queue_name (str): the name of the queue
        tweet (str): the tweet to be sent to the queue
    """
    try:
        # create a blocking connection to the RabbitMQ server
        conn = pika.BlockingConnection(pika.ConnectionParameters(host))
        # use the connection to create a communication channel
        ch = conn.channel()
        # use the channel to declare a durable queue
        # a durable queue will survive a RabbitMQ server restart
        # and help ensure messages are processed in order
        # messages will not be deleted until the consumer acknowledges
        ch.queue_declare(queue=queue_name, durable=True)
        # use the channel to publish a message to the queue
        # every message passes through an exchange
        ch.basic_publish(exchange="", routing_key=queue_name, body=tweet.encode())
        # print a message to the console for the user
        print(f" [x] Sent {tweet}")
    except pika.exceptions.AMQPConnectionError as e:
        print(f"Error: Connection to RabbitMQ server failed: {e}")
    finally:
        # close the connection to the server
        conn.close()

if __name__ == "__main__":
    # read from the csv file to get tweet data
    with open('tweets.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            tweet = row[0]
            send_tweet('localhost', 'tweets', tweet)

