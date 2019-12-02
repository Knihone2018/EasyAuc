import pika, json
from user import *

#docker run -d --hostname my-rabbit --name some-rabbit -p 15672:15672 -p 5672:5672 rabbitmq:3-management

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()


# a function to check the validity of the user: if the user is deleted or blocked, send True; otherwise send False
"""
    Incoming json requirement: 
        userId: int
"""
channel.queue_declare(queue='checkuser')
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

channel.basic_consume(queue='checkuser', on_message_callback=check_user_valid_request)



# a function to return the email of the user
"""
    Incoming json requirement: 
        userId: int
"""
channel.queue_declare(queue='email-address')
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

channel.basic_consume(queue='email-address', on_message_callback=get_user_email)



# a function to add items to shopping cart
# use point to point
"""
    Incoming json requirement: 
        userId: int
        itemId: int
        quantity: int
        buy_now: int
"""
channel.queue_declare(queue='add_item_to_cart_queue')

def add_item_to_cart(ch, method, properties, body):
    info = json.loads(body)
    userId = info['userId']
    itemId = info['itemId']
    addQuantity = info['quantity']
    isBid = 1 - int(info['buy_now'])

    print(" [x] addToCart(%s)" % userId)
    ctl = CartControl()
    res = ctl.addToCart(userId, itemId, addQuantity, isBid)

channel.basic_consume(queue='add_item_to_cart_queue', on_message_callback=add_item_to_cart, auto_ack=True)



print(" [x] Awaiting requests...")
channel.start_consuming()
