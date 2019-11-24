import mysql.connector
from flask import Flask, request, jsonify, Response
from datetime import datetime
import threading
import json
import os,base64
from flask_cors import CORS #pip install -U flask-cors
# import pika
# import uuid

# Item:
# ID
# sellerID
# name
# category
# quantity
# cur_price
# price_step
# start_time
# end_time
# flag
# buy_now
# buy_now_price
# shipping_cost
# sold
# description

#Category:
# ID
# name

class DatabaseControl:
	def CreateTable(self):
		self.CreateDatabase()
		self.Getdb()
		self.CreateCategoryTable()
		self.CreateItemTable()

	def Getdb(self):
		mydb = mysql.connector.connect(
		  host="localhost",
		  user="root",
		  passwd="123456",
		  database="ITEM"
		)
		self.db = mydb
		return mydb

	def CreateDatabase(self):
		mydb = mysql.connector.connect(
		  host="localhost",
		  user="root",
		  passwd="123456"
		)
		mycursor = mydb.cursor()
		mycursor.execute("CREATE DATABASE IF NOT EXISTS ITEM")

	def CreateCategoryTable(self):
		self.db.cursor().execute("create table if not exists Category (ID int auto_increment primary key,\
			 					name varchar(255), index(name))")
		# self.db.cursor().execute("create unique index cate_name on Category (name)")
		# self.db.commit()

	def CreateItemTable(self):
		self.db.cursor().execute("create table if not exists Item (\
										ID int auto_increment primary key,\
										sellerID int,\
		 								name varchar(255) unique,\
		 								category int,\
		 								quantity int default 1,\
										cur_price float,\
										price_step float,\
										start_time datetime,\
										end_time datetime,\
						 				flag int default 0,\
										buy_now boolean default False,\
										buy_now_price int default 0,\
										sent_to_auc boolean default False,\
										shipping_cost int,\
										description varchar(1000),\
										url varchar(1000),\
										status boolean default True,\
										photo varchar(1000),\
										index(name,url),index(category),\
										index(start_time,buy_now,sent_to_auc),\
										foreign key(category) references Category(ID))")

class ItemControl(DatabaseControl):
	def AddItem(self, item):
		db = self.Getdb()
		cursor = db.cursor()
		#check name
		stored = self.SearchByName(item['name'])
		if stored:
			return "Name Already Exists"
        
		#insert
		sql = "insert into Item (sellerID, name, category, quantity, cur_price, start_time, end_time, buy_now, buy_now_price, shipping_cost, description)\
			 	values (%(sellerID)s, %(name)s, %(category)s,%(quantity)s,%(cur_price)s,%(start_time)s,%(end_time)s,%(buy_now)s,%(buy_now_price)s,%(shipping_cost)s,%(description)s)"
		cursor.execute(sql,item)
		db.commit()
		
		#get itemID
		res = self.SearchByName(item['name'])

		# add photo
		png = "/photo/%d.png"%res
		with open(png,'wb') as f:
			f.write(base64.b64decode(item["photo"]))

		sql = "update Item set photo = {} where ID = {}".format(png,res)
		cursor.execute(sql,item)
		db.commit()			
		return res
	
	def UpdatePrice(self, info):
		db = self.Getdb()
		#update cur_price
		sql = "UPDATE Item SET cur_price = %(cur_price)s WHERE ID = %(ID)s"
		db.cursor().execute(sql,info)
		db.commit()
		return True		

	def UpdateStatus(self, info):
		db = self.Getdb()
		#update status
		sql = "UPDATE Item SET status = False WHERE ID = %(ID)s"
		db.cursor().execute(sql,info)
		db.commit()
		return True	

	def UpdateQuantity(self, info):
		db = self.Getdb()
		#update status
		sql = "UPDATE Item SET quantity = %(quantity)s WHERE ID = %(ID)s"
		db.cursor().execute(sql,info)
		db.commit()
		return True	

	def SearchByName(self, name):
		db = self.Getdb()
		cursor = db.cursor(buffered=True)
		#get ID
		cursor.execute("select ID from Item where name=\"%s\""%name)
		res = cursor.fetchone()
		if res:
			return res[0]
		else:
			return None

	def GetUrl(self,name):
		db = self.Getdb()
		cursor = db.cursor(buffered=True)
		#get ID
		cursor.execute("select url from Item where name=\"%s\""%name)
		res = cursor.fetchone()
		if res:
			return res[0]
		else:
			return None		

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
		return Item

	def SearchByCategory(self,category):
		db = self.Getdb()
		cursor = db.cursor(buffered=True)		
		#get item
		sql = "select name,price,url,photo from Item where status=True and url is not null and category = {}".format(category)
		cursor.execute(sql)
		res = cursor.fetchall() # a tuple of tuples
		return res


	def SearchByFlag(self):
		db = self.Getdb()
		cursor = db.cursor(buffered=True)		
		#get item
		sql = "select ID,name,category,flag,url from Item where flag > 0"
		cursor.execute(sql)
		res = cursor.fetchall() # a tuple of tuples
		return res




#category
class CategoryControl(DatabaseControl):
	def AddCategory(self,name):
		db = self.Getdb()
		mycursor = db.cursor()
		#check name
		if self.GetId(name):
			return False
		#add
		sql = "insert into Category (name) values {}".format(name)
		mycursor.execute(sql)
		db.commit()
		return True

	def ModifyCategory(self,old,new):
		db = self.Getdb()
		mycursor = db.cursor()
		#check old name
		if not self.GetId(old):
			return "Old Name Not Exist"
		#check new name
		if self.GetId(new):
			return "New Name Duplicate"	
		#add
		sql = "update Category set name = {} where name = {}".format(new,old)
		mycursor.execute(sql)
		db.commit()
		return True

	def DeleteCategory(self, name):
		db = self.Getdb()
		mycursor = db.cursor()
		if not self.GetId(name):
			return "Not Exist"
		try:
			sql = "DELETE FROM Category WHERE name = {}".format(name)
			mycursor.execute(sql)
			db.commit()
			return True
		except:
			return "Existing Item Related"

	def GetId(self,name):
		db = self.Getdb()
		mycursor = db.cursor()
		mycursor.execute("select ID from Category where name=\"%s\""%name)
		res = mycursor.fetchone()
		if res:
			return res[0]
		else:
			return None

	def GetCategory(self):
		db = self.Getdb()
		mycursor = db.cursor()
		mycursor.execute("select * from Category")
		res = mycursor.fetchall() # a tuple of tuples
		return res






#RabitMQ connection
class RabitMQ_PUB:
	# point to point
	def start_auction(self,message):
		connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
		channel = connection.channel()
		channel.exchange_declare(exchange='AuctionStart', exchange_type='fanout')
		channel.basic_publish(exchange='AuctionStart', routing_key='', body=message)
		print(" Start an auction: %r" % message)
		connection.close()


class RabitMQ_RPC():
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
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
    
    def checkuser(self, user_id):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='checkuser',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body='{"userId":{}}'.format(user_id))
        while self.response is None:
            self.connection.process_data_events()
        return self.response





#Check Auction Start in DB
def CheckAuctionStart():
	db = DatabaseControl().Getdb()
	mycursor = db.cursor()
	mycursor.execute("select ID from Item where buy_now = false and start_time <= \'%s\' and sent_to_auc = false"%datetime.now())
	res = mycursor.fetchall()

	for id in res:
		mycursor.execute("update table set sent_to_auc=true where ID = {}".format(id[0]))
		db.commit()
		#publish
		message = {"ID":id[0],"buy_now":False}
		RabitMQ_PUB().start_auction(json.dumps(message))








#run Flask
app = Flask(__name__)
CORS(app)

############################################# with auction
#get url

#update current price
@app.route("/updateprice", methods=["PUT"])
# ID: int
# cur_price : int
def updateprice():
	req = request.json
	#item control
	ctl = ItemControl()
	res = ctl.UpdatePrice(req)
	message = {"success":res}
	return jsonify(message)

#update status
@app.route("/updatestatus", methods=["PUT"])
# ID: int
# status : bool
def updatestatus():
	req = request.json
	#item control
	ctl = ItemControl()
	res = ctl.UpdateStatus(req)
	return Response(json.dumps(res), status=200)
#############################################

# update quantity with user

#############################################

#add item POST
@app.route("/additem", methods=["POST"])
# incoming request format: Json
# sellerID:int
# name:string
# category:string
# quantity:int
# cur_price:float
# price_step:float
# start_time:datetime
# end_time:datetime
# buy_now:bool
# buy_now_price:int
# shipping_cost:int
# description:string
# photo:string (base64)
def additem():
	req = request.json

	#check if user valid first
	RPC = RabitMQ_RPC()
	if RPC.checkuser(req['sellerID']) == 'True':
		message = {"success":False,"message":"sellerID is invalid"}
		return Response(json.dumps(message), status=400)

	# check category
	category = req['category']
	cat_id = CategoryControl().GetId(category)
	if not cat_id:
		message = {"success":False,"message":"Category Not Exists"}
		return Response(json.dumps(message), status=400)

	#update dictionary
	req['category'] = cat_id
	req["start_time"] = datetime.fromtimestamp(req["start_time"])
	req["end_time"] = datetime.fromtimestamp(req["end_time"])
	#item control
	ctl = ItemControl()
	res = ctl.AddItem(req)

	Publish = RabitMQ_PUB()		
	#send to auction immediately if buy now item
	if req["buy_now"]:
		message = {'itemID':res,"buy_now":req["buy_now"]}
		Publish.start_auction(json.dumps(message))

	message = {"success":True,"message":res}
	return jsonify(message)

#get Item by ID
@app.route("/getitembyid", methods=["GET"])
# ID: int
def getitembyid():
	req = request.json
	#item control
	ctl = ItemControl()
	res = ctl.SearchByID(req["ID"])
	return jsonify(res)

#get items by category
@app.route("/searchbycategory", methods=["GET"])
# categoryID : int
def searchbycategory():
	req = request.json
	#item control
	ctl = ItemControl()
	res = ctl.SearchByCategory(req['categoryID'])
	dic = {}
	for item in res:
		dic[item[0]] = item[1:]
	message = {"success":True,"message":dic}
	return jsonify(message)


#get auctions by name
@app.route("/searchbyname", methods=["GET"])
# categoryID : int
def searchbyname():
	req = request.json
	#item control
	ctl = ItemControl()
	res = ctl.GetUrl(req['name'])
	message = None
	if res:
		message = {"success":True,"message":res}
	else:
		message = {"success":False}
	return jsonify(message)


#get auctions by name
@app.route("/searchbyflag", methods=["GET"])
# categoryID : int
def searchbyflag():
	req = request.json
	#item control
	ctl = ItemControl()
	res = ctl.SearchByFlag()
	dic = {}
	for item in res:
		dic[item[0]] = item[1:]
	message = {"success":True,"message":dic}
	return jsonify(message)


#get all categories
@app.route("/allcategory", methods=["GET"])
# input:None
# output: json
def getcategory():
	#category control
	catectl = CategoryControl()
	res = catectl.GetCategory()
	dic = {}
	for category in res:
		dic[category[0]] = category[1]
	message = {"success":True,"message":dic}
	return jsonify(message)


#add category
@app.route("/addcategory", methods=["POST"])
# name: string
def addcategory():
	req = request.json
	#category control
	catectl = CategoryControl()
	res = catectl.AddCategory(req)
	message = {"success":res}
	return jsonify(message)


#modify category
@app.route("/modifycategory", methods=["PUT"])
# ID: int
def modifycategory():
	req = request.json
	#category control
	catectl = CategoryControl()
	res = catectl.ModifyCategory(req["old_name"],req["new_name"])
	message = None
	if res == "Old Name Not Exist":
		message = {"success":False,"message":res}
	elif res == "New Name Duplicate":
		message = {"success":False,"message":res}
	else:
		message = {"success":True}
	return jsonify(message)


#delete category
@app.route("/deletecategory", methods=["DELETE"])
# ID: int
def deletecategory():
	req = request.json
	#category control
	catectl = CategoryControl()
	res = catectl.DeleteCategory(req["name"])
	if res == "Not Exist":
		message = {"success":False,"message":res}
	elif res == "Existing Item Related":
		message = {"success":False,"message":res}
	else:
		message = {"success":True}
	return jsonify(message)		





# Run the Flask application as a server.
if __name__ == "__main__":
	#create database
	DBctl = DatabaseControl()
	DBctl.CreateTable()

	#check auction start
	t = threading.Timer(60, CheckAuctionStart)
	t.start()

	#create a photo directory
	filename = "/photo"
	os.makedirs(os.path.dirname(filename), exist_ok=True)

	#flask
	p = 9000
	app.run(port=p)
