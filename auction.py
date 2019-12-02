from app import app, db
from app.models import Auction, Bid
import threading
import pika
import json
from datetime import datetime
from app.routes import add_to_cart_RabbitMQ
from app.routes import get_item
from app.routes import get_seller_id
from app.routes import status_info


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Auction': Auction, 'Bid': Bid}


# mark auction complete, and add item to cart
def do_after_auction_end(auction_id):
    auction = Auction.query.filter_by(id=auction_id).first()
    if auction:
        auction.completed = True
        db.session.commit()

        # send auction status to item microservice
        status_info(auction.item_id)

        # add item to cart when auction ends
        buy_now = auction.buy_now
        if not buy_now:
            highest_bid = auction.current_price
            bid = Bid.query.filter_by(bid_amount=highest_bid).first()
            if bid:
                user_id = bid.bidder_id
                item_id = auction.item_id
                add_to_cart_RabbitMQ(user_id, item_id, 0, 1)

def send_countdown_to_RabbitMQ(email_info):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='172.17.0.2'))
    channel = connection.channel()

    channel.queue_declare(queue='email')

    channel.basic_publish(exchange='', routing_key='email', body=email_info)
    print(" [x] Sent countdown to RabbitMQ")
    print(email_info)
    connection.close()    


# notify bidder and seller countdown
def countdown(auction_id, countdown_type):
    auction = Auction.query.filter_by(id=auction_id).first_or_404()
    if not auction.completed:
        item_id = auction.item_id
        seller_id = get_seller_id(item_id)
        bids = auction.bids
        id_list = []
        id_list.append(str(seller_id))
        for bid in bids:
            bidder_id = bid.bidder_id
            id_list.append(str(bidder_id))
        id_string = ",".join(id_list)
        #auction_url = 'localhost:5000/auction/{}'.format(auction_id)
        auction_url ='www.google.com'
        email_info = {
            "user_id" : id_string,
            "type" : countdown_type,
            "url": auction_url
        }
        send_countdown_to_RabbitMQ(json.dumps(email_info))


# item was sent to RabbitMQ, once auction starts
def consume_item_from_RabbitMQ():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='172.17.0.2'))
    channel = connection.channel()
    channel.exchange_declare(exchange='AuctionStart', exchange_type='fanout')
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange='AuctionStart', queue=queue_name)
    
    print(' [*] Waiting for items. To exit press CTRL+C')

    def callback(ch, method, properties, body):
        items = json.loads(body)
        item_id = items['ID']
        buy_now = items['buy_now']
        end_time = items['end_time']
        if not Auction.query.filter_by(item_id=item_id).first():
            print(" [x] Loading item {} to Auction Table.".format(item_id)) 
            auction = Auction(item_id=item_id, end_time=end_time, buy_now=buy_now)        
            db.session.add(auction)
            db.session.commit()
            # send auction url information to item microservice
            auction_id = auction.id
            time_left = auction.time_left()
            threading.Timer(max(time_left, 0.), do_after_auction_end, [auction.id]).start()
                
            one_day_left = auction.time_left() - 3600*24
            one_hour_left = auction.time_left() - 3600
            if one_day_left >= 0:
                threading.Timer(one_day_left, countdown, [auction.id, "oneDayCountDown"]).start()
            if one_hour_left >= 0:
                threading.Timer(one_hour_left, countdown, [auction.id, "oneHourCountDown"]).start()
                    
            print(" [x] Item {} loaded to Auction Table.".format(item_id))          

    channel.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=True)

    channel.start_consuming()


if __name__ == '__main__':
    threading.Thread(target=consume_item_from_RabbitMQ).start()
    app.run(host='0.0.0.0', port=5000)
