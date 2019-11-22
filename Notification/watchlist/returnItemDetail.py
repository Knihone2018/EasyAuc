#!/usr/bin/env python3
import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='172.17.0.2')
)

channel = connection.channel()
channel.queue_declare(queue='getItemDetail')

test = {"1234": {"item_id": "1", "item_name": "macBook", "category": "computer", "imageUrl": "https://www.google.com/url?sa=i&rct=j&q=&esrc=s&source=images&cd=&ved=2ahUKEwiV1Ibw7_zlAhVKnKwKHXUeBtgQjRx6BAgBEAQ&url=https%3A%2F%2Fwww.apple.com%2Fshop%2Fbuy-mac%2Fmacbook-pro&psig=AOvVaw1UBb0sBjOv43hKmNIEG9ux&ust=1574479638681742",
"price": "1200", "auctionUrl": "www.apple.com"}, 
"2": {"item_id": "2", "item_name": "lego", "category": "toy", "imageUrl": "https://www.google.com/imgres?imgurl=https%3A%2F%2Fwww.lego.com%2F_build%2Fpublic%2FGrownUps-1ef120e14ea511d005529b60261647b1.png&imgrefurl=https%3A%2F%2Fwww.lego.com%2Fen-us%2Fproduct%2Fdinosaur-fossils-21320&docid=fQhDe4wZleImiM&tbnid=kwltUHLUB-iKZM%3A&vet=10ahUKEwikv77N8PzlAhUCP6wKHVWiDUgQMwiAAygBMAE..i&w=782&h=600&client=safari&bih=1017&biw=1920&q=lego&ved=0ahUKEwikv77N8PzlAhUCP6wKHVWiDUgQMwiAAygBMAE&iact=mrc&uact=8",
"price": "100", "aunctionUrl": "www.lego.com"},
"3": {"item_id": "3", "item_name": "dyson", "category": "electric", "imageUrl": "https://www.google.com/imgres?imgurl=https%3A%2F%2Fimages-na.ssl-images-amazon.com%2Fimages%2FI%2F61jiXeUPtjL._SL1500_.jpg&imgrefurl=https%3A%2F%2Fwww.amazon.com%2FDyson-Cyclone-Lightweight-Cordless-Cleaner%2Fdp%2FB0798LCJK9&docid=jJQDwwPphOEJXM&tbnid=2kPdV2GLJg5BkM%3A&vet=10ahUKEwjn546a8fzlAhUC5awKHZ5cDdMQMwj1AigAMAA..i&w=1500&h=1500&client=safari&bih=1017&biw=1920&q=dyson&ved=0ahUKEwjn546a8fzlAhUC5awKHZ5cDdMQMwj1AigAMAA&iact=mrc&uact=8",
"price": "300", "auntionUrl": "www.dyson.com"}}

def on_request(ch, method, props, body):
    items = body.decode("utf-8").split(",")
    print("Got {}".format(items))
    itemsDetail = []
    for item in items:
        if item in test.keys():
            itemDetail = test[item]
            print(itemDetail)
            itemsDetail.append(itemDetail)
    response = {"Itmes": itemsDetail}
    print(response)

    ch.basic_publish(exchange='', 
    routing_key=props.reply_to,
    properties=pika.BasicProperties(correlation_id = props.correlation_id),
    body=str(response))

    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='getItemDetail', on_message_callback=on_request)

print("Start!")
channel.start_consuming()