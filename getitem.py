import mysql.connector
from flask import Flask, request, jsonify, Response
import json
from flask_cors import CORS
import pika
import uuid

class RabitMQ_RPC():
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='172.17.0.2'))
        self.channel = self.connection.channel()
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue = self.callback_queue,
            on_message_callback = self.on_response,
            auto_ack = True
        )

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body
    
    def getemail(self, user_id):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='email-address',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=json.dumps({"userId":user_id}))
        while self.response is None:
            self.connection.process_data_events()
        return self.response


class DatabaseControl:
	def Getdb(self):
		mydb = mysql.connector.connect(
		  host="localhost",
		  user="root",
		  passwd="123456",
		  database="ITEM"
		)
		self.db = mydb
		return mydb

class ItemControl(DatabaseControl):
    def SearchByID(self, ID):
        db = self.Getdb()
        cursor = db.cursor(buffered=True)
        #get item
        sql = "select * from Item where ID = %d" %ID
        cursor.execute(sql)
        res = cursor.fetchone()
        Item = {
            "ID":res[0],
            "sellerID":res[1],
            "name":res[2],
            "category":res[3],
            "quantity":res[4],
            "cur_price":res[5],
            "price_step":res[6],
            "start_time":res[7],
            "end_time":res[8],
            "flag":res[9],
            "buy_now":res[10],
            "buy_now_price":res[11],
            "sent_to_auc":res[12],
            "shipping_cost":res[13],
            "description":res[14],
            "url":res[15],
            "status":res[16],
            "photo":res[17]
            }
        ctl = CategoryControl()
        name = ctl.GetName(Item["category"])
        Item["category"] = name
        return Item                                       

#category
class CategoryControl(DatabaseControl):
	def GetName(self,id):
		db = self.Getdb()
		mycursor = db.cursor()
		mycursor.execute("select name from Category where ID=\"%s\""%id)
		res = mycursor.fetchone()
		if res:
			return res[0]
		else:
			return None    


#run Flask
app = Flask(__name__)
CORS(app)

#get Item by ID
@app.route("/getitembyid", methods=["GET"])
# ID: int
def getitembyid():
	req = request.json
	#item control
	ctl = ItemControl()
	res = ctl.SearchByID(req["ID"])
	return jsonify(res)


#get Item by ID
@app.route("/getemail", methods=["GET"])
# ID: int
def getemail():
  req = request.json
  if not req["ID"]:
    return {"success":False,"message":"Empty User"}
  res = RabitMQ_RPC().getemail(req["ID"])
  dic = {"Email":res}
  return jsonify(dic)


# Run the Flask application as a server.
if __name__ == "__main__":
	#flask
	p = 9001
	app.run(host="172.17.0.5",port=p)
