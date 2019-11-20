import pika, json
from user import *

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='rpc_get_user_deleted_or_blocked_queue')

# a function to check the validity of the user: if the user is deleted or blocked, send True; otherwise send False
#        a string of json object
#        e.g: '{"userId":2}'
def check_user_valid_request(ch, method, props, body):
    b = json.loads(body)
    userId = b['userId']

    print(" [.] check_user_valid_request(%s)" % userId)
    ctl = AccountControl()
    blocked = ctl.checkBlockByUserId(userId)
    deleted = ctl.checkDeleteByUserId(userId)
    response = False if blocked == 0 and deleted == 0 else True

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='rpc_get_user_deleted_or_blocked_queue', on_message_callback=check_user_valid_request)



# a function to return the email of the user
# parameter of body: 
#        a string of json object
#        e.g: '{"userId":2}'
channel.queue_declare(queue='rpc_get_user_email_queue')
def get_user_email(ch, method, props, body):
    b = json.loads(body)
    userId = b['userId']

    print(" [.] getUserEmailbyUserId(%s)" % userId)
    ctl = AccountControl()
    response = ctl.getUserEmailbyUserId(userId)

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='rpc_get_user_email_queue', on_message_callback=get_user_email)


print(" [x] Awaiting RPC requests")
channel.start_consuming()

