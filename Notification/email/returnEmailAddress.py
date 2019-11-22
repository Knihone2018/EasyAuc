#!/usr/bin/python3
import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='172.17.0.2'))

channel = connection.channel()
channel.queue_declare(queue='emailaddress')

emailList = {"123": "angbian16@gmail.com", "999": "angbian@uchicago.edu"}

def on_request(ch, method, props, body):
    id = body.decode("utf-8") 
    print("Got user: " + id)
    if id in emailList.keys():
        response = emailList[id]
    else:
        response = "ang.bian96@gmail.com"
    
    ch.basic_publish(exchange='', routing_key=props.reply_to, 
    properties=pika.BasicProperties(correlation_id = props.correlation_id),
    body = response)

    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='emailaddress', on_message_callback=on_request)

print("service starts!")
channel.start_consuming()