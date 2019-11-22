#!/usr/bin/env python3
import pika
import uuid
import json

class GetItemDetail():
    
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='172.17.0.2'))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='getItemDetail')
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue = self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True
        )

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body
    
    def call(self, items):
        print(items)
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key = 'getItemDetail',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=str(items)
        )
        while self.response is None:
            self.connection.process_data_events()
        # res = json.loads(self.response)
        # return res
        print(self.response)
        return self.response.decode('utf-8').replace("'", "\"")

getItemDetail = GetItemDetail()

items = "1,2"
print(items)
response = getItemDetail.call(items)
print(response)