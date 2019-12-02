import mysql.connector
from flask import Flask, request, jsonify, Response
from datetime import datetime
import threading
import json
from flask_cors import CORS
import pika
import uuid



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
# sent_to_auc
# shipping_cost
# description
# url
# status
# photo

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

	def CreateItemTable(self):
		self.db.cursor().execute("create table if not exists Item (\
										ID int not null auto_increment primary key,\
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
										url varchar(255),\
										status boolean default True,\
										photo varchar(255),\
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
		sql = "insert into Item (sellerID, name, category, quantity, cur_price, price_step,\
			 					start_time, end_time, buy_now, buy_now_price, shipping_cost, description, photo)\
			 	values (%(sellerId)s, %(name)s, %(category)s, %(quantity)s, %(cur_price)s, %(price_step)s,\
					 	%(start_time)s, %(end_time)s, %(buy_now)s, %(buy_now_price)s, %(shipping_cost)s, %(description)s, %(photo)s)"
		cursor.execute(sql,item)
		db.commit()
		
		#get itemID
		res = self.SearchByName(item['name'])

		url = ''
		if item['buy_now']:
			url = 'buynow.html?itemId={}'.format(res)
		else:
			url = 'auction.html?itemId={}'.format(res)
		sql = "UPDATE Item SET url = '{}' WHERE ID = {}".format(url,res)
		db.cursor().execute(sql)
		db.commit()		
		return res
	

	def UpdatePrice(self, itemID, price):
		db = self.Getdb()
		#update cur_price
		sql = "UPDATE Item SET cur_price = {} WHERE ID = {}".format(price,itemID)
		db.cursor().execute(sql)
		db.commit()
		return True		

	def UpdateStatus(self, itemID):
		db = self.Getdb()
		#update status
		sql = "UPDATE Item SET status = False WHERE ID = {}".format(itemID)
		db.cursor().execute(sql)
		db.commit()
		return True	

	def UpdateQuantity(self,itemID,quantity):
		db = self.Getdb()
		#update status
		sql = "UPDATE Item SET quantity = {} WHERE ID = {}".format(quantity,itemID)
		db.cursor().execute(sql)
		db.commit()
		return True	


	def UpdateDescription(self,itemID,desc):
		db = self.Getdb()
		sql = "UPDATE Item SET description = '{}' WHERE ID = {}".format(desc,itemID)
		db.cursor().execute(sql)
		db.commit()
		return True			


	def UpdateShipping(self,itemID,ship):
		db = self.Getdb()
		sql = "UPDATE Item SET shipping_cost = {} WHERE ID = {}".format(ship,itemID)
		db.cursor().execute(sql)
		db.commit()
		return True


	def UpdateFlag(self,itemID):
		db = self.Getdb()
		sql = "UPDATE Item SET flag = flag+1 WHERE ID = {}".format(itemID)
		db.cursor().execute(sql)
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


	def GetItemByName(self,name):
		db = self.Getdb()
		cursor = db.cursor(buffered=True)		
		#get item
		sql = "select ID,name,cur_price,url,photo from Item where status=True and url is not null and name = '{}'".format(name)
		cursor.execute(sql)
		res = cursor.fetchone() 
		if res:
			return res
		else:
			return None		


	def GetUserItem(self,sellerID):
		db = self.Getdb()
		cursor = db.cursor(buffered=True)		
		#get item
		sql = "select ID,name,buy_now,quantity,shipping_cost,description from Item where status=True and sellerID = {}".format(sellerID)
		cursor.execute(sql)
		res = cursor.fetchall() 
		if res:
			return res
		else:
			return None	


	def SearchByCategory(self,category):
		db = self.Getdb()
		cursor = db.cursor(buffered=True)		
		#get item
		sql = "select ID,name,cur_price,url,photo from Item where status=True and url is not null and category = {}".format(category)
		cursor.execute(sql)
		res = cursor.fetchall() # a tuple of tuples
		return res


	def SearchByFlag(self):
		db = self.Getdb()
		cursor = db.cursor(buffered=True)		
		#get item
		sql = "select i.ID, i.name, c.name, i.flag, i.url from Item i join Category c on i.category = c.ID where i.flag > 0"
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
		sql = "insert into Category (name) values ('{}')".format(name)
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
		sql = "update Category set name = '{}' where name = '{}'".format(new,old)
		mycursor.execute(sql)
		db.commit()
		return True

	def DeleteCategory(self, name):
		db = self.Getdb()
		mycursor = db.cursor()
		ID = self.GetId(name)
		if not ID:
			return "Not Exist"
		
		ctl = ItemControl()
		if ctl.SearchByCategory(ID):
			return "Existing Item Related"

		sql = "DELETE FROM Category WHERE name = '{}'".format(name)
		mycursor.execute(sql)
		db.commit()
		return True
			

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
'''
point to point
get url
update current price
json: {'head':'price','itemID':10,'new_price':15.5}

update status
json: {'head':'status','itemID':10}
'''
class RabitMQ_Point:
	def callback(self,ch, method, properties, body):
		print(" [x] Received %r" % body)
		content = json.loads(body)
		ctl = ItemControl()
		if content['head'] == 'price':
			ctl.UpdatePrice(content['itemID'],content['new_price'])
		elif content['head'] == 'status':
			ctl.UpdateStatus(content['itemID'])

	def updateWithAuction(self):
		connection = pika.BlockingConnection(pika.ConnectionParameters(host='172.17.0.2'))
		channel = connection.channel()
		channel.queue_declare(queue='ItemAuction')

		channel.basic_consume(queue='ItemAuction', on_message_callback=self.callback, auto_ack=True)

		print('Thread Waiting for Auction to Update')
		channel.start_consuming()

# run in a thread
def withAuction():
	point = RabitMQ_Point()
	point.updateWithAuction()



class RabitMQ_PUB:
	def start_auction(self,message):
		print(" Start an auction: %r" % message)
		connection = pika.BlockingConnection(pika.ConnectionParameters(host='172.17.0.2'))
		channel = connection.channel()
		channel.exchange_declare(exchange='AuctionStart', exchange_type='fanout')
		channel.basic_publish(exchange='AuctionStart', routing_key='', body=message)
		connection.close()


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
#json: {"ID":10,"buy_now":False/True}

def CheckAuctionStart():
	db = DatabaseControl().Getdb()
	mycursor = db.cursor()
	mycursor.execute("select ID from Item where buy_now = false and start_time <= \'%s\' and sent_to_auc = false"%datetime.now())
	res = mycursor.fetchall()

	for id in res:
		mycursor.execute("update Item set sent_to_auc=true where ID = {}".format(id[0]))
		db.commit()
		#publish
		message = {"ID":id[0],"buy_now":False}
		RabitMQ_PUB().start_auction(json.dumps(message))









#run Flask
app = Flask(__name__)
CORS(app)



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
# photo:string
def additem():
	# store image
	# img_file = request.files.get('file')
	# png = "C:\\Uchicago\\Topics in Software Engineering\\iteration3\\%d.png"%1
	# img_file.save(png)

	req = request.json
	#check if user valid first
	# RPC = RabitMQ_RPC()
	# if RPC.checkuser(req['sellerID']) == 'True':
	# 	message = {"success":False,"message":"sellerID is invalid"}
	# 	return jsonify(message)

	# check category
	category = req['category']
	cat_id = CategoryControl().GetId(category)
	if not cat_id:
		message = {"success":False,"message":"Category Not Exists"}
		return jsonify(message)

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


#get seller items
#{"success":True,"message":{ID:[name,buy_now,quantity,shipping_cost,description]}}
@app.route("/getselleritem/<ID>", methods=["GET"])
def getselleritem(ID):
	ctl = ItemControl()
	res = ctl.GetUserItem(ID)
	dic = {}
	for item in res:
		dic[item[0]] = item[1:]
	message = {"success":True,"message":dic}
	return jsonify(message)


#update Item
@app.route("/updateitem", methods=["PUT"])
def updateitem():
	req = request.json
	ctl = ItemControl()
	ctl.UpdateDescription(req["ID"],req["description"])
	ctl.UpdateQuantity(req["ID"],req["quantity"])
	ctl.UpdateShipping(req["ID"],req["shipping_cost"])
	message = {"success":True}
	return jsonify(message)


#get items by category
@app.route("/searchbycategory/<categoryID>", methods=["GET"])
# categoryID : int
def searchbycategory(categoryID):
	#item control
	ctl = ItemControl()
	res = ctl.SearchByCategory(categoryID)
	dic = {}
	for item in res:
		dic[item[0]] = item[1:]
	message = {"success":True,"message":dic}
	print(message)
	return jsonify(message)


#get auctions by name
@app.route("/searchbyname/<name>", methods=["GET"])
# categoryID : int
def searchbyname(name):
	#item control
	ctl = ItemControl()
	res = ctl.GetItemByName(name)
	message = None
	print(res)
	if res:
		dic = {}
		dic[res[0]] = res[1:]
		message = {"success":True,"message":dic}
	else:
		message = {"success":False}
	print(message)
	return jsonify(message)


#increase flag on an item
@app.route("/setflag", methods=["PUT"])
# categoryID : int
def setflag():
	req = request.json
	#item control
	ctl = ItemControl()
	ctl.UpdateFlag(req["ID"])
	message = {"success":True}
	return jsonify(message)


#get all flaged items
@app.route("/searchbyflag", methods=["GET"])
# categoryID : int
def searchbyflag():
	#item control
	ctl = ItemControl()
	res = ctl.SearchByFlag()
	print(res)
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
	print(req)
	#category control
	catectl = CategoryControl()
	res = catectl.AddCategory(req["name"])
	message = {"success":res}
	return jsonify(message)


#modify category
@app.route("/modifycategory", methods=["PUT"])
# ID: int
def modifycategory():
	req = request.json
	print(req)
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
	print(req)
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
	t1 = threading.Timer(60, CheckAuctionStart)
	t1.start()

	#update with auction
	t2 = threading.Thread(target = withAuction)
	t2.start()

	#flask
	p = 9000
	app.run(host="0.0.0.0",port=p)
