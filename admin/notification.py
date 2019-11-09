from flask_restful import reqparse, abort, Resource

class Notification(Resource):
	def send_email(self):
		return "sss"