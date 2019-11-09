from flask import Flask
from flask_restful import Resource, Api
from flagged_item import FlaggedItemList, FlaggedItem
from category import CategoryList, Category
from auction import AuctionList, Auction
from user import UserList, User
from notification import Notification

app = Flask(__name__)
api = Api(app)

api.add_resource(FlaggedItemList, '/item')
api.add_resource(FlaggedItem, '/item/<item_id>')
api.add_resource(CategoryList, '/category')
api.add_resource(Category, '/category/<category_id>')
api.add_resource(AuctionList, '/auction')
api.add_resource(Auction, '/auction/<auction_id>')
api.add_resource(UserList, '/user')
api.add_resource(User, '/user/<user_id>')
api.add_resource(Notification, '/notification')

if __name__ == '__main__':
    app.run(debug=True)