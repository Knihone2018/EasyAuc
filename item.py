import mysql.connector
import itertools
import string
import hashlib
from flask import Flask, request, jsonify, Response
import json
from datetime import datetime

class Item:
	def __init__(self):
		self.ID = None
		self.name = None
		self.category = None
		self.flag = None
		self.quantity = None
		self.price = None
		self.start_time = None
		self.end_time = None
		self.rating = None
		self.status = None
		self.buy_now = None
		self.shipping_cost = None
		self.tag = None

class Category:
	def __init__(self):
		self.ID = None
		self.name = None

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
										cur_price int not null,\
										start_time datetime,\
										end_time datetime,\
										total_rating int,\
										rating_count int,\
						 				flag int default 0,\
										buy_now boolean default False,\
										buy_now_price int default 0,\
										shipping_cost int,\
										status boolean default True,\
										description varchar(1000),\
										index(name),index(category),\
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
		sql = "UPDATE Item SET cur_price = %(status)s WHERE ID = %(ID)s"
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

	def SearchByCategory(self, name):
		db = self.Getdb()
		#get item
		db.cursor().execute("SELECT Item.ID, Item.sellerID, Item.name, Category.name, Item.quantity, Item.cur_price,\
			 				Item.start_time, Item.end_time, Item.buy_now, Item.buy_now_price, Item.shipping_cost, Item.description\
							from Item left join Category on Item.category = Category.ID where Category.name = %s"%name)
		res = db.cursor().fetchall()
		return res

class CategoryControl(DatabaseControl):
	def AddCategory(self,category):
		db = self.Getdb()
		mycursor = db.cursor()
		sql = "insert into Category (name) values (%(name)s)"
		mycursor.execute(sql,category)
		db.commit()
		#get categoryID
		res = self.getid(category['name'])
		return res

	def DeleteCategory(self, category):
		try:
			db = self.Getdb()
			sql = "DELETE FROM Category WHERE ID = %(ID)s"
			db.cursor().execute(sql,category)
			db.commit()
			return True
		except:
			return False

	def getid(self,name):
		db = self.Getdb()
		mycursor = db.cursor()
		mycursor.execute("select ID from Category where name=\"%s\""%name)
		res = mycursor.fetchone()
		if res:
			return res[0]
		else:
			return None

#run Flask
app = Flask(__name__)

#add item POST
@app.route("/additem", methods=["POST"])
#incoming request format: Json
#key includes: 
# sellerID:int
# name:string
# category:string
# quantity:int
# cur_price:int
# start_time:datetime
# end_time:datetime
# buy_now:bool
# buy_now_price:int
# shipping_cost:int
# description:string
def additem():
	req = request.json
	#get category
	category = req['category']
	cat_id = CategoryControl().getid(category)
	if not cat_id:
		res = "Category Not Exists"
	else:
		#update dictionary
		req['category'] = cat_id
		req["start_time"] = datetime.fromtimestamp(req["start_time"])
		req["end_time"] = datetime.fromtimestamp(req["end_time"])
		#item control
		ctl = ItemControl()
		res = ctl.AddItem(req)
	return Response(json.dumps(res), status=200)

#update current price
@app.route("/updateprice", methods=["PUT"])
# ID: int
# cur_price : int
def updateprice():
	req = request.json
	#item control
	ctl = ItemControl()
	res = ctl.UpdatePrice(req)
	return Response(json.dumps(res), status=200)

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

#get items by category
@app.route("/searchbycategory", methods=["GET"])
# name : string
def searchbycategory():
	req = request.json
	#item control
	ctl = ItemControl()
	res = ctl.SearchByCategory(req['name'])
	return Response(json.dumps(res), status=200)	

#add category
@app.route("/addcategory", methods=["POST"])
# name: string
def addcategory():
	req = request.json
	#category control
	catectl = CategoryControl()
	res = catectl.AddCategory(req)
	return Response(json.dumps(res), status=200)

#delete category
@app.route("/deletecategory", methods=["DELETE"])
# ID: int
def deletecategory():
	req = request.json
	#category control
	catectl = CategoryControl()
	res = catectl.DeleteCategory(req)
	return Response(json.dumps(res), status=200)


# Run the Flask application as a server.
if __name__ == "__main__":
	p = 9000
	DBctl = DatabaseControl()
	DBctl.CreateTable()
	app.run(port=p)
