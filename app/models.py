from app import db
from datetime import datetime

class Auction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, unique=True)
    end_time = db.Column(db.DateTime)
    completed = db.Column(db.Boolean, default=False)
    current_price = db.Column(db.Float)
    # bids return all the bids on this auction
    # target can return all the bids that a user has bid on
    bids = db.relationship('Bid', backref='target', lazy='dynamic')

    def time_left(self):
        delta = self.end_time - datetime.utcnow()
        return delta.total_seconds()

    def next_price(self, price_step):
        return self.current_price + price_step

    def n_bids(self):
        return self.bids.count()


class Bid(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    auction_id = db.Column(db.Integer, db.ForeignKey('auction.id'))
    bidder_id = db.Column(db.Integer, index=True)
    bidder_name = db.Column(db.String(10), index=True)
    bid_amount = db.Column(db.Float)
    time_stamp = db.Column(db.DateTime, default=datetime.utcnow)
