import csv
import kafka

from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

with open('data.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)  # skip the header row
    for row in reader:
        message = ','.join(row).encode('utf-8')
        producer.send('my_topic', message)
