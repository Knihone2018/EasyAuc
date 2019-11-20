from flask import render_template, flash, redirect, url_for
from app import app, db
from app.forms import BidForm, BuyForm
from app.models import Auction, Bid
from datetime import datetime, timedelta
from sqlalchemy import func
from hashlib import md5
import random
import threading

# only logged in user can see the auction page.

digest = md5('1'.encode('utf-8')).hexdigest()
items = {
    1: {'item_name': 'Harry Potter',
        'item_image': 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, 128),
        'seller_id': 1,
        'start_time': datetime.utcnow(),
        'end_time': datetime.utcnow() + timedelta(seconds=15),
        'current_price': 35.0,
        'price_step': 5.,
        'buy_now': False,
        'quantity': 10},
    2: {'item_name': 'NBA 2K20',
        'item_image': 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, 128),
        'seller_id': 2,
        'start_time': datetime.utcnow(),
        'end_time': datetime.utcnow() + timedelta(seconds=20),
        'current_price': 59.99,
        'price_step': 1.0,
        'buy_now': True,
        'quantity': 50},
    3: {'item_name': 'Canon 77D',
        'item_image': 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, 128),
        'seller_id': 3,
        'start_time': datetime.utcnow(),
        'end_time': datetime.utcnow() + timedelta(seconds=30),
        'current_price': 699.99,
        'price_step': 10.0,
        'buy_now': False,
        'quantity': 30},
    4: {'item_name': 'Nikon 5600',
        'item_image': 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, 128),
        'seller_id': 4,
        'start_time': datetime.utcnow(),
        'end_time': datetime.utcnow() + timedelta(seconds=40),
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
    return items[item_id]


def get_user(user_id):
    return users[user_id]

# create a pseudo shopping cart
carts = dict()
for key in users:
    carts[key] = list()

# place item to shopping cart
def add_to_cart(user_id, item_id):
    carts[user_id].append(item_id)

def mark_auction_completed(auction_id):
    print('auction_id = {}'.format(auction_id))
    auction = Auction.query.filter_by(id=auction_id).first_or_404()
    auction.completed = True
    db.session.commit()

# put all the items in auction table
# only when the item is not in auction table
# for now, don't care the situation that one item has many historical auctions
@app.before_first_request
def load_items():
    for key, value in items.items():
        if not Auction.query.filter_by(item_id=key).first():
            auction = Auction(item_id=key, end_time=value['end_time'])
            db.session.add(auction)
            db.session.commit()
            time_left = auction.time_left()
            threading.Timer(max(time_left, 0.), mark_auction_completed, [auction.id]).start()
print('loaded item into auction table')

# get current user id from frontend
curr_user_id = random.randint(1, 7)
print('curr_user_id: {}'.format(curr_user_id))

@app.route('/auction/<auction_id>', methods=['GET', 'POST'])
def auction(auction_id):
    auction = Auction.query.filter_by(id=auction_id).first_or_404()
    item_id = auction.item_id
    # get item using item_id
    item = get_item(item_id)

    # for bid item
    if not item['buy_now']:
        bid_form = BidForm()
        # if no bids on the auction, use the current_price in item
        if auction.bids.count() == 0:
            auction.current_price = item['current_price']
            db.session.commit()
        else:
            auction.current_price = db.session.query(func.max(Bid.bid_amount))\
                .filter(Bid.auction_id == auction_id).scalar()
            db.session.commit()

        if bid_form.validate_on_submit():
            bid_amount = bid_form.bid_amount.data
            # only commit bid that are larger than next_price
            if bid_amount >= auction.next_price(item['price_step']):
                curr_user = get_user(curr_user_id)
                bid = Bid(auction_id=auction_id, bidder_id=curr_user_id, bidder_name=curr_user['user_name'],
                          bid_amount=bid_amount, time_stamp=datetime.utcnow())
                db.session.add(bid)
                db.session.commit()
                flash('Congratulations, you have placed a bid!')
                auction.current_price = bid_amount
                db.session.commit()
            else:
                flash('Please enter a higher bid!')
            return redirect(url_for('auction', auction_id=auction_id))
        return render_template('auction.html', form=bid_form, auction=auction, item=item, curr_user_id=curr_user_id)

    else:  # for buy now item
        buy_form = BuyForm()
        auction.current_price = item['current_price']
        db.session.commit()
        if buy_form.validate_on_submit():
            quantity = buy_form.quantity.data
            if quantity <= item['quantity']:
                curr_user = get_user(curr_user_id)
                bid = Bid(auction_id=auction_id, bidder_id=curr_user_id, bidder_name=curr_user['user_name'],
                          bid_amount=item['current_price'], time_stamp=datetime.utcnow())
                db.session.add(bid)
                db.session.commit()
                flash('Congratulations, you have bought an item!')
                # add buy now item to cart
                add_to_cart(curr_user_id, auction.item_id)
                print(carts)
            else:
                flash('Please enter a valid quantity!')
            return redirect(url_for('auction', auction_id=auction_id))
        return render_template('auction.html', form=buy_form, auction=auction, item=item, curr_user_id=curr_user_id)


@app.route('/auction/<auction_id>/bids', methods=['GET'])
def bids(auction_id):
    auction = Auction.query.filter_by(id=auction_id).first_or_404()
    current_bids = auction.bids.all()
    return render_template('bids.html', bids=current_bids)


# add item to watchlist, add to a RabbitMQ
@app.route('/auction/<auction_id>/add_to_watchlist/<user_id>')
def add_to_watchlist(auction_id, user_id):
    flash('Item has been added to watchlist.')
    return redirect(url_for('auction', auction_id=auction_id))
