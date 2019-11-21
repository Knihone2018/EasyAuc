import pika
import uuid,json


# an example of client rpc calls of get email function

class Test(object):

    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body


    # parameter of body: 
    #        a string of json object
    #        e.g: '{"userId":2}'
    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='rpc_get_user_deleted_or_blocked_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body='{"userId":2}')
        while self.response is None:
            self.connection.process_data_events()
        return self.response


test_rpc = Test()

print(" [x] Requesting ...")
response = test_rpc.call(1)
print(" [.] Got %r" % response)

