from app import db
from datetime import datetime
from hashlib import md5


class Auction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, unique=True)
    auction_title = db.Column(db.String(100))
    seller_id = db.Column(db.Integer, unique=True)
    start_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    end_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    current_price = db.Column(db.Float)
    price_step = db.Column(db.Float)
    bids = db.relationship('Bid', backref='target', lazy='dynamic')

    def image(self, size):
        digest = md5(str(self.item_id).encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def time_left(self):
        seconds = (self.end_time - datetime.utcnow()).total_seconds()
        return divmod(seconds, 3600)[0]

    def next_price(self):
        return self.current_price + self.price_step


class Bid(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    auction_id = db.Column(db.Integer, db.ForeignKey('auction.id'))
    bidder_id = db.Column(db.Integer, index=True)
    bidder_name = db.Column(db.String(10), index=True)
    bid_amount = db.Column(db.Float)
    time_stamp = db.Column(db.DateTime, default=datetime.utcnow)
