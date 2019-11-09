from flask_restful import reqparse, abort, Resource

class AuctionList(Resource):
	def get(self):
		return "sss"

class Auction(Resource):
	def get(self, auction_id):
		return "sss"