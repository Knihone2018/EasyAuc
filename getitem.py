import mysql.connector
from flask import Flask, request, jsonify, Response
import json
from flask_cors import CORS


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

# Run the Flask application as a server.
if __name__ == "__main__":
	#flask
	p = 9001
	app.run(host="172.17.0.3",port=p)
