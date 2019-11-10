from app import app, db
from app.models import Auction, Bid


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Auction': Auction, 'Bid': Bid}
