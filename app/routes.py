from flask import render_template
from app import app
from app.forms import BidForm
from app.models import Auction


@app.route('/auction/<auction_id>', methods=['GET', 'POST'])
def auction(auction_id):
    form = BidForm()
    auction = Auction.query.filter_by(id=auction_id).first_or_404()
    return render_template('auction.html', form=form, auction=auction)
