#!/usr/bin/python3

import pika
import json
import pymongo

# Compare items with parameters
def compare(item_name, min_price, max_price, item):
    if int(min_price) > int(item['price']) or int(max_price) < int(item['price']):
        return "-1"
    newName = item['item_name'].upper().split(" ")
    name = item_name.upper().split(" ")
    count = 0
    for keyword in name:
        if keyword in newName:
            count = count + 1
    if count/len(name) > 0.3:
        return item['item_id']
    else:
        return "-1"

# Add items to watchlist
def addNew(ch, method, properties, body):
    item = json.loads(body)
    results = paraCollection.find({'category': item['category']})
    users = []
    for result in results:
        add = compare(result['item_name'], result['min_price'], result['max_price'], item)
        if add != "-1":
            new = {'user_id': result['user_id'], 'item_id': add}
            itemCollection.insert_one(new)
            print("add to " + result['user_id'])
            users.append(result['user_id'])
    
    user_ids = ",".join(users)
    sendEmail(user_ids, item['url'])

# Send email to notify
def sendEmail(id, item_url):
    emailChannel = connection.channel()
    emailChannel.queue_declare(queue='email')
    emailInfo = '{' + '"user_id": "{}", "type": "watchlist", "url": "{}"'.format(id, item_url) + '}'
    emailChannel.basic_publish(exchange='', routing_key='email', body=emailInfo)
    print("sent email to {}".format(emailInfo))
    
dbClient = pymongo.MongoClient(host='localhost', port=27017)
watchlist_db = dbClient["watchlist"]
itemCollection = watchlist_db['items']
paraCollection = watchlist_db["parameters"]

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='172.17.0.2'))
channel = connection.channel()

channel.queue_declare(queue='watchlist')
channel.basic_consume(
    queue='watchlist', on_message_callback=addNew, auto_ack=True)
print("Service start!")
channel.start_consuming()
