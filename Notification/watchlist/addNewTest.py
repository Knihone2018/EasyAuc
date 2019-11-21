#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='172.17.0.2'))
channel = connection.channel()

channel.queue_declare(queue='watchlist')

itemInfo = '{"item_id": "12300", "item_name": "Macbookpro 256GB 2015", "category": "computer", "price": "1000", "url":"www.google.com"}'

channel.basic_publish(exchange='', routing_key='watchlist', body=itemInfo)
print(" [x] Sent 'item'")
connection.close()
