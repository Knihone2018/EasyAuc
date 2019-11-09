from flask_restful import reqparse, abort, Resource

class FlaggedItemList(Resource):
	def get(self):
		return ["1"]

class FlaggedItem(Resource):
	def get(self, item_id):
		return ["2"]