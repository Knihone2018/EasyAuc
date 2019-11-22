#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='172.17.0.2'))
channel = connection.channel()

channel.queue_declare(queue='email')

emailInfo = '{"user_id": "999,123,567", "type": "toSeller", "url": "www.google.com"}'

channel.basic_publish(exchange='', routing_key='email', body=emailInfo)
print(" [x] Sent 'Email'")
connection.close()
