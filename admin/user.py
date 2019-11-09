from flask_restful import reqparse, abort, Resource

class UserList(Resource):
	def get(self):
		return "sss"

class User(Resource):
	def get(self, user_id):
		return "sss"