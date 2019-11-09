from flask_restful import reqparse, abort, Resource

class CategoryList(Resource):
	def get(self):
		return "1"

class Category(Resource):
	def get(self, category_id):
		return "sss"

	def delete(self, category_id):
		return "success"

	def put(self, category_id):
		return "success"