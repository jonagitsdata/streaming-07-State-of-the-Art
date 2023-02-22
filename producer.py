import pika
import sys
import webbrowser
import csv
import time


#####################################################################################

# define variables for host, smoker_temp, food_a_temp, food_b_temp, 
host = "localhost"
tweet_queue = 'tweety_bird'
csv_file = 'tweets.csv'
show_offer = True #Define if you want to have the RabbitMQ Admit site opened, True = Y, False = N

######################################################################################

# define option to open rabbitmq admin site
def offer_rabbitmq_admin_site(show_offer):
    if show_offer == True:
    
        """Offer to open the RabbitMQ Admin website"""
        ans = input("Would you like to monitor RabbitMQ queues? y or n ")
        print()
        if ans.lower() == "y":
                webbrowser.open_new("http://localhost:15672/#/queues")
                print()

##########################################################################################

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

