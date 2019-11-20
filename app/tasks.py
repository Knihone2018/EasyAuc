import threading
from datetime import datetime, timedelta
from app.models import Auction
from app import db

def mark_auction_completed(auction_id):
    print('Before threading:')
    print(Auction.query.filter_by(id=1).first_or_404().completed)
    auction = Auction.query.filter_by(id=auction_id).first_or_404()
    auction.completed = True
    db.session.commit()
    print('After threading:')
    print(Auction.query.filter_by(id=1).first_or_404().completed)

auctions = Auction.query.all()
for auction in auctions:
    threading.Timer(10.0, mark_auction_completed, [auction.id]).start()