#!/usr/bin/python3
import pika
import uuid

class GetEmail():

    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='172.17.0.2'))
        self.channel = self.connection.channel()
        result = self.channel.queue_declare(queue='emailaddress')
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue = self.callback_queue,
            on_message_callback = self.on_response,
            auto_ack = True
        )

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body
    
    def call(self, user_id):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='emailaddress',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=user_id)
        while self.response is None:
            self.connection.process_data_events()
        return self.response.decode("utf-8") 
