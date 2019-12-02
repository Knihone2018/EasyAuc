from flask import render_template, flash, redirect, url_for, jsonify
from flask import request
from app import app, db
from app.forms import BidForm, BuyForm
from app.models import Auction, Bid
from datetime import datetime, timedelta
from sqlalchemy import func
from hashlib import md5
import random
import pika
import sys
import json
import requests


# only logged in user can see the auction page.

digest = md5('1'.encode('utf-8')).hexdigest()
items = {
    1: {'item_name': 'Harry Potter',
        'item_image': 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, 128),
        'seller_id': 1,
        'start_time': datetime.utcnow(),
        'end_time': datetime.utcnow() + timedelta(seconds=50),
        'current_price': 35.0,
        'price_step': 5.,
        'buy_now': False,
        'quantity': 10},
    2: {'item_name': 'NBA 2K20',
        'item_image': 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, 128),
        'seller_id': 2,
        'start_time': datetime.utcnow(),
        'end_time': datetime.utcnow() + timedelta(seconds=60),
        'current_price': 59.99,
        'price_step': 1.0,
        'buy_now': True,
        'quantity': 50},
    3: {'item_name': 'Canon 77D',
        'item_image': 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, 128),
        'seller_id': 3,
        'start_time': datetime.utcnow(),
        'end_time': datetime.utcnow() + timedelta(seconds=70),
        'current_price': 699.99,
        'price_step': 10.0,
        'buy_now': False,
        'quantity': 30},
    4: {'item_name': 'Nikon 5600',
        'item_image': 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, 128),
        'seller_id': 4,
        'start_time': datetime.utcnow(),
        'end_time': datetime.utcnow() + timedelta(seconds=80),
        'current_price': 599.99,
        'price_step': 0.50,
        'buy_now': True,
        'quantity': 1},
}

users = {
    1: {'user_name': 'AA',
        'logged_in': True},
    2: {'user_name': 'BB',
        'logged_in': True},
    3: {'user_name': 'CC',
        'logged_in': True},
    4: {'user_name': 'DD',
        'logged_in': True},
    5: {'user_name': 'EE',
        'logged_in': True},
    6: {'user_name': 'FF',
        'logged_in': True},
    7: {'user_name': 'GG',
        'logged_in': True}
}


def get_item(item_id):
    itemdic = {"ID":item_id}
    p = requests.get(url=f"http://172.17.0.5:9001/getitembyid", json=itemdic)
    item = json.loads(p.text)
    #item = items[item_id]
    return item

def get_seller_id(item_id):
    item = get_item(item_id)
    seller_id = item['sellerID']
    return seller_id

def get_user(user_id):
    user_id = int(user_id)
    return users[user_id]


# create a pseudo shopping cart
carts = dict()
for key in users:
    carts[key] = list()

# place item to shopping cart
def add_to_cart_RabbitMQ(user_id, item_id, buy_now, quantity):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='172.17.0.2'))
    channel = connection.channel()
    channel.queue_declare(queue='add_item_to_cart_queue')
    message = {
        "userId" : user_id,
        "itemId" : item_id,
        "buy_now" : buy_now,
        "quantity" : quantity
    }
    message = json.dumps(message)
    channel.basic_publish(exchange='', routing_key='add_item_to_cart_queue', body=message)
    print(" [x] Sent %r to cart" % message)
    connection.close() 

# send auction information to item microservice
def send_auction_info_to_RabbitMQ(message):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='172.17.0.2'))
    channel = connection.channel()

    channel.queue_declare(queue='ItemAuction')

    channel.basic_publish(exchange='', routing_key='ItemAuction', body=message)
    print(" [x] Sent auction information to RabbitMQ")
    connection.close()

# send current price to RabbitMQ
def current_price_info(item_id, current_price):
    message = {
        'head' : 'price',
        'itemID' : item_id,
        'new_price' : current_price
    }
    send_auction_info_to_RabbitMQ(json.dumps(message))


# send status to RabbitMQ
def status_info(item_id):
    message = {
        'head' : 'status',
        'itemID' : item_id
    }
    send_auction_info_to_RabbitMQ(json.dumps(message))

# send bid information to notification microservice
def send_bid_info_to_RabbitMQ(email_info):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='172.17.0.2'))
    channel = connection.channel()

    channel.queue_declare(queue='email')

    channel.basic_publish(exchange='', routing_key='email', body=email_info)
    print(" [x] Sent bid_info to RabbitMQ")
    print(email_info)
    connection.close()


# notify bidder and seller countdown
def bid_info(auction_id, user_id, to_whom):
    auction = Auction.query.filter_by(id=auction_id).first_or_404()
    auction_url = 'www.google.com'
    email_info = {
        "user_id" : str(user_id),
        "type" : to_whom,
        "url": auction_url
    }
    send_bid_info_to_RabbitMQ(json.dumps(email_info))   


@app.route('/auction/<item_id>', methods=['GET'])
def auction(item_id):
    user_id = request.args.get('userId')
    auction = Auction.query.filter_by(item_id=item_id).first_or_404()
    auction_id = auction.id
    # get item using item_id
    item = get_item(int(item_id))

    # for bid item
    if not item['buy_now']:
        # if no bids on the auction, use the current_price in item
        if auction.bids.count() == 0:
            auction.current_price = item['cur_price']
            db.session.commit()
        else:
            auction.current_price = db.session.query(func.max(Bid.bid_amount))\
                .filter(Bid.auction_id == auction_id).scalar()
            db.session.commit()

        message = {
            'success' : True,
            'item_name' : item['name'],
            'end_time' : auction.end_time.strftime("%Y-%m-%d %H:%M:%S"),
            'time_left' : auction.time_left(),
            'current_price' : auction.current_price,
            'price_step' : item['price_step'],
            'image_url' : item['photo'],
            'shipping_cost' : item['shipping_cost'],
            'description' : item['description']
        }
        print(message)
    else:  # for buy now item
        auction.current_price = item['buy_now_price']
        db.session.commit()

        message = {
            'success' : True,
            'item_name' : item['name'],
            'end_time' : auction.end_time.strftime("%Y-%m-%d %H:%M:%S"),
            'time_left' : auction.time_left(),
            'current_price' : auction.current_price,
            'quantity' : item['quantity'],
            'image_url' : item['photo'],
            'shipping_cost' : item['shipping_cost'],
            'description' : item['description']
        }
        print(message)
    return jsonify(message)


@app.route('/place_bid', methods=['POST'])
def place_bid():
    bid_data = json.loads(request.data)
    print(bid_data)
    item_id = int(bid_data['item_id'])
    auction = Auction.query.filter_by(item_id=item_id).first_or_404()
    auction_id = auction.id
    # get item using item_id
    item = get_item(item_id)

    bid_amount = bid_data['bid']
    # only commit bid that are larger than next_price
    if bid_amount and bid_amount >= auction.next_price(item['price_step']):
        curr_user_id = bid_data['user_id']
        bid = Bid(auction_id=auction_id, bidder_id=curr_user_id, bidder_name='xx',
                  bid_amount=bid_amount, time_stamp=datetime.utcnow())
        db.session.add(bid)
        db.session.commit()
        # notify previous highest bidder
        prev_bid = Bid.query.filter_by(bid_amount=auction.current_price).first()
        if prev_bid:
            bid_info(auction_id, prev_bid.bidder_id, "toBidder")

        auction.current_price = bid_amount
        db.session.commit()
        # send current price to RabbitMQ, if bid placed
        current_price_info(item_id, auction.current_price)
        # send email to bidder
        bid_info(auction_id, get_seller_id(item_id), "toSeller")
    return jsonify({'success':True})


@app.route('/buy_now', methods=['POST'])
def buy_now():
    print(request)
    buy_data = request.json
    print(buy_data)
    item_id = int(buy_data['item_id'])
    auction = Auction.query.filter_by(item_id=item_id).first_or_404()
    auction_id = auction.id
    # get item using item_id
    item = get_item(item_id)
    quantity = buy_data['quantity']
    if quantity <= item['quantity']:
        curr_user_id = buy_data['user_id']
        bid = Bid(auction_id=auction_id, bidder_id=curr_user_id, bidder_name='xx',
                  bid_amount=item['cur_price'], time_stamp=datetime.utcnow())
        db.session.add(bid)
        db.session.commit()
        # add buy now item to cart
        add_to_cart_RabbitMQ(curr_user_id, item_id, 1, quantity)
    return jsonify({'success':True}) 
    

@app.route('/auction/<item_id>/bids', methods=['GET'])
def bids(item_id):
    auction = Auction.query.filter_by(item_id=item_id).first_or_404()
    current_bids = auction.bids.all()
    bids_list = []
    for current_bid in current_bids:
        bidder_id = current_bid.bidder_id
        bid_amount = current_bid.bid_amount
        time_stamp = current_bid.time_stamp
        bids_list.append({'bidder_id':bidder_id, 'bid_amount':bid_amount, 'time_stamp':time_stamp})

    message = {
        'success' : True,
        'bids' : bids_list
    }
    return jsonify(message)
