import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='add_item_to_cart_queue')

channel.basic_publish(exchange='', routing_key='add_item_to_cart_queue', body='{"userId":1, "itemId":23, "quantity":1, "buy_now": 1}')
print(" [x] Sent add item to cart request.")
connection.close()