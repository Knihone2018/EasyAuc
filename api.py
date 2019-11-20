from flask import Flask, request, Response, jsonify
from flasgger import Swagger
from nameko.standalone.rpc import ClusterRpcProxy
import pika
from user import *



app = Flask(__name__)
Swagger(app)
Port = 5672
#CONFIG = {'AMQP_URI': "amqp://guest:guest@localhost"}



####################################################
# restful apis
####################################################



######################
# Getters for Account Database
######################

"""
Incoming json requirement:
    userId: int
Response:
    a response class of Flask
        userId: int
"""
@app.route("/checkdeleteaccount", methods=["GET"])
def checkDeleteAccount():
    userId = request.json.get('userId')
    ctl = AccountControl()
    res = ctl.checkDeleteByUserId(userId)
    if res != -1:
        return Response(json.dumps({'value': res}), status = 200)
    return "There has been an error"


"""
Incoming json requirement:
    userId: int
Response:
    a response class of Flask
        userId: int
"""

@app.route("/checkblockaccount", methods=["GET"])
def checkBlockAccount():
    userId = request.json.get('userId')
    ctl = AccountControl()
    res = ctl.checkBlockByUserId(userId)
    if res != -1:
        return Response(json.dumps({'value': res}), status = 200)
    return "There has been an error"


"""
Incoming json requirement:
    userId: int
Response:
    a response class of Flask
        userId: int
"""
@app.route("/getuseremail", methods=["GET"])
def getUserEmail():
    userId = request.json.get('userId')
    ctl = AccountControl()
    res = ctl.getUserEmailbyUserId(userId)
    print(res)
    if res:
        return Response(json.dumps({'value': res}), status = 200)
    return "There has been an error"


"""
Incoming json requirement:
    userId: int
Response:
    a response class of Flask
        userId: int
"""
@app.route("/getuserfirstname", methods=["GET"])
def getUserFirstname():
    userId = request.json.get('userId')
    ctl = AccountControl()
    res = ctl.getUserFirstname(userId)
    if res:
        return Response(json.dumps({'value': res}), status = 200)
    return "There has been an error"


"""
Incoming json requirement:
    userId: int
Response:
    a response class of Flask
        userId: int
"""
@app.route("/getuserlastname", methods=["GET"])
def getUserLastname():
    userId = request.json.get('userId')
    ctl = AccountControl()
    res = ctl.getUserLastname(userId)
    if res:
        return Response(json.dumps({'value': res}), status = 200)
    return "There has been an error"


"""
Incoming json requirement:
    userId: int
Response:
    a response class of Flask
        userId: int
"""
@app.route("/getuserpassword", methods=["GET"])
def getUserPassword():
    userId = request.json.get('userId')
    ctl = AccountControl()
    res = ctl.getUserPassword(userId)
    if res:
        return Response(json.dumps({'value': res}), status = 200)
    return "There has been an error"


"""
Incoming json requirement:
    userId: int
Response:
    a response class of Flask
        userId: int
"""
@app.route("/getuseraddress", methods=["GET"])
def getUserAddress():
    userId = request.json.get('userId')
    ctl = AccountControl()
    res = ctl.getUserAddress(userId)
    if res:
        return Response(json.dumps({'value': res}), status = 200)
    return "There has been an error"



"""
Incoming json requirement:
    userId: int
Response:
    a response class of Flask
        userId: int
"""
@app.route("/getuserzipcode", methods=["GET"])
def getUserZipcode():
    userId = request.json.get('userId')
    ctl = AccountControl()
    res = ctl.getUserZipcode(userId)
    if res:
        return Response(json.dumps({'value': res}), status = 200)
    return "There has been an error"


"""
Incoming json requirement:
    userId: int
Response:
    a response class of Flask
        userId: int
"""
@app.route("/getusercity", methods=["GET"])
def getUserCity():
    userId = request.json.get('userId')
    ctl = AccountControl()
    res = ctl.getUserCity(userId)
    if res:
        return Response(json.dumps({'value': res}), status = 200)
    return "There has been an error"



"""
Incoming json requirement:
    userId: int
Response:
    a response class of Flask
        userId: int
"""
@app.route("/getuserstate", methods=["GET"])
def getUserState():
    userId = request.json.get('userId')
    ctl = AccountControl()
    res = ctl.getUserState(userId)
    if res:
        return Response(json.dumps({'value': res}), status = 200)
    return "There has been an error"


"""
Incoming json requirement:
    userId: int
Response:
    a response class of Flask
        userId: int
"""
@app.route("/getuserbankaccount", methods=["GET"])
def getUserBankAccNum():
    userId = request.json.get('userId')
    ctl = AccountControl()
    res = ctl.getUserBankAccNum(userId)
    if res:
        return Response(json.dumps({'value': res}), status = 200)
    return "There has been an error"


######################
# Setters for Account Database
######################


"""
Incoming json requirement:
    email: string
    firstname: string
    lastname: string
    password: string
    address: string
    zipcode: int
    city: string
    state: string
    bankAccountNumber: int
    isBlocked: boolean
    isDeleted: boolean
    isAdmin: boolean
    ratingSum: int
    numOfRates: int
Response:
    a response class of Flask
        userId: int
"""
@app.route("/addaccount", methods=["POST"])
def addAccount():
    email = "" if request.json.get('email') is None else request.json.get('email')
    firstname = "" if request.json.get('firstname') is None else request.json.get('firstname')
    lastname = "" if request.json.get('lastname') is None else request.json.get('lastname')
    password = "" if request.json.get('password') is None else request.json.get('password')
    address = "" if request.json.get('address') is None else request.json.get('address')
    zipcode = -1 if request.json.get('zipcode') is None else request.json.get('zipcode')
    city = "" if request.json.get('city') is None else request.json.get('city')
    state = "" if request.json.get('state') is None else request.json.get('state')
    bankAccountNumber = -1 if request.json.get('bankAccountNumber') is None else request.json.get('bankAccountNumber')
    isBlocked = 0 if request.json.get('isBlocked') is None else request.json.get('isBlocked')
    isDeleted = 0 if request.json.get('isDeleted') is None else request.json.get('isDeleted')
    isAdmin = 0 if request.json.get('isAdmin') is None else request.json.get('isAdmin')
    ctl = AccountControl()
    res = ctl.addAccount(email, firstname, lastname, password, address, zipcode, city, state, bankAccountNumber, isBlocked, isDeleted, isAdmin, 0, 0)
    if res:
        return Response(json.dumps({'userId': res}), status = 200)
    return "There has been an error"


"""
Incoming json requirement:
    userId: int
Response:
    a response class of Flask
        userId: int
"""
@app.route("/deleteaccount", methods=["POST"])
def deleteAccount():
    userId = request.json.get('userId')
    ctl = AccountControl()
    res = ctl.deleteAccount(userId)
    if res:
        return Response(json.dumps({'userId': res}), status = 200)
    return "There has been an error"



"""
Incoming json requirement:
    userId: int
Response: 
    200
    description: successfully block user
"""
@app.route('/blockaccount', methods=['POST'])
def blockAccount():
    userId = request.json.get('userId')
    ctl = AccountControl()
    res = ctl.blockAccount(userId)
    if res:
        return Response(json.dumps({'userId': res}), status = 200)
    return "There has been an error"



"""
Incoming json requirement:
    userId: int
    rate: int
Response:
    a response class of Flask
        userId: int
"""
@app.route("/addsellerrate", methods=["POST"])
def addOneSellerRating():
    userId = request.json.get('userId')
    newNum = request.json.get('rate')
    ctl = AccountControl()
    res = ctl.addRating(userId, newNum)
    if res:
        return Response(json.dumps({'userId': userId}), status = 200)
    return "There has been an error"



"""
Incoming json requirement:
    userId: int
    email: string
Response:
    a response class of Flask
        userId: int
"""
@app.route("/setemail", methods=["POST"])
def setEmail():
    userId = request.json.get('userId')
    newemail = request.json.get('email')
    ctl = AccountControl()
    res = ctl.setEmail(userId, newemail)
    if res:
        return Response(json.dumps({'userId': userId, 'newemail': newemail}), status = 200)
    return "There has been an error"



"""
Incoming json requirement:
    userId: int
    firstName: string
Response:
    a response class of Flask
        userId: int
"""
@app.route("/setfirstname", methods=["POST"])
def setFirstname():
    userId = request.json.get('userId')
    newStr = request.json.get('firstName')
    ctl = AccountControl()
    res = ctl.setFirstname(userId, newStr)
    if res:
        return Response(json.dumps({'userId': userId}), status = 200)
    return "There has been an error"



"""
Incoming json requirement:
    userId: int
    lastName: string
Response:
    a response class of Flask
        userId: int
"""
@app.route("/setlastname", methods=["POST"])
def setLastname():
    userId = request.json.get('userId')
    newStr = request.json.get('lastName')
    ctl = AccountControl()
    res = ctl.setLastname(userId, newStr)
    if res:
        return Response(json.dumps({'userId': userId}), status = 200)
    return "There has been an error"


"""
Incoming json requirement:
    userId: int
    password: string
Response:
    a response class of Flask
        userId: int
"""
@app.route("/setlastname", methods=["POST"])
def setPassword():
    userId = request.json.get('userId')
    newStr = request.json.get('password')
    ctl = AccountControl()
    res = ctl.setPassword(userId, newStr)
    if res:
        return Response(json.dumps({'userId': userId}), status = 200)
    return "There has been an error"


"""
Incoming json requirement:
    userId: int
    address: string
Response:
    a response class of Flask
        userId: int
"""
@app.route("/setaddress", methods=["POST"])
def setAddress():
    userId = request.json.get('userId')
    newStr = request.json.get('address')
    ctl = AccountControl()
    res = ctl.setAddress(userId, newStr)
    if res:
        return Response(json.dumps({'userId': userId}), status = 200)
    return "There has been an error"


"""
Incoming json requirement:
    userId: int
    zipcode: int
Response:
    a response class of Flask
        userId: int
"""
@app.route("/setzipcode", methods=["POST"])
def setZipcode():
    userId = request.json.get('userId')
    newNum = request.json.get('zipcode')
    ctl = AccountControl()
    res = ctl.setZipcode(userId, newNum)
    if res:
        return Response(json.dumps({'userId': userId}), status = 200)
    return "There has been an error"


"""
Incoming json requirement:
    userId: int
    city: String
Response:
    a response class of Flask
        userId: int
"""
@app.route("/setcity", methods=["POST"])
def setCity():
    userId = request.json.get('userId')
    newStr = request.json.get('city')
    ctl = AccountControl()
    res = ctl.setCity(userId, newStr)
    if res:
        return Response(json.dumps({'userId': userId}), status = 200)
    return "There has been an error"



"""
Incoming json requirement:
    userId: int
    state: String
Response:
    a response class of Flask
        userId: int
"""
@app.route("/setstate", methods=["POST"])
def setState():
    userId = request.json.get('userId')
    newStr = request.json.get('state')
    ctl = AccountControl()
    res = ctl.setState(userId, newStr)
    if res:
        return Response(json.dumps({'userId': userId}), status = 200)
    return "There has been an error"



"""
Incoming json requirement:
    userId: int
    BankAccNum: int
Response:
    a response class of Flask
        userId: int
"""
@app.route("/setbankaccountnum", methods=["POST"])
def setBankAccNum():
    userId = request.json.get('userId')
    newNum = request.json.get('BankAccNum')
    ctl = AccountControl()
    res = ctl.setBankAccNum(userId, newNum)
    if res:
        return Response(json.dumps({'userId': userId}), status = 200)
    return "There has been an error"





######################
# Setters for Cart Database
######################

"""
Incoming json requirement:
    userId: int
    itemId: int
    addQuantity: int
Response:
    a response class of Flask
        userId: int
"""
@app.route("/additemtocartfrombuynow", methods=["POST"])
def addItemToCartFromBuynow():
    userId = request.json.get('userId')
    itemId = request.json.get('itemId')
    addQuantity = request.json.get('addQuantity')
    ctl = CartControl()
    res = ctl.addToCart(userId, itemId, addQuantity, 0)
    if res:
        return Response(json.dumps({'userId': userId}), status = 200)
    return "There has been an error"



"""
Incoming json requirement:
    userId: int
    itemId: int
    addQuantity: int
    isBid: boolean
Response:
    a response class of Flask
        userId: int
"""
@app.route("/deleteitemfromcart", methods=["POST"])
def deleteItemFromCart():
    userId = request.json.get('userId')
    itemId = request.json.get('itemId')
    addQuantity = request.json.get('addQuantity')
    isBid = request.json.get('isBid')
    ctl = CartControl()
    if ctl.checkItemIsBid(userId, itemId):
        return "Cannot delete an item won from a bid"
    res = ctl.deleteFromCart(userId, itemId, addQuantity, isBid)
    if res:
        return Response(json.dumps({'userId': userId}), status = 200)
    return "There has been an error"



"""
Incoming json requirement:
    userId: int
Response:
    a response class of Flask
        userId: int
"""
@app.route("/emptycart", methods=["POST"])
def emptyShoppingCart():
    userId = request.json.get('userId')
    ctl = CartControl()
    res = ctl.emptyCart(userId)
    if res:
        ## need to call restful api in Item to update quantity!
        return Response(json.dumps({'userId': userId}), status = 200)
    return "There has been an error"




######################
# Getters for Cart Database
######################


"""
Incoming json requirement:
    userId: int
    itemId: int
Response:
    a response class of Flask
        userId: int
"""
@app.route("/getitemisbid", methods=["GET"])
def getItemIsBid():
    userId = request.json.get('userId')
    itemId = request.json.get('itemId')
    ctl = CartControl()
    res = ctl.checkItemIsBid(userId, itemId)
    if res != -1:
        return Response(json.dumps({'value': res}), status = 200)
    return "There has been an error"



"""
Incoming json requirement:
    userId: int
    itemId: int
Response:
    a response class of Flask
        userId: int
"""
@app.route("/getoneitemincart", methods=["GET"])
def getOneItemInfoInCart():
    userId = request.json.get('userId')
    itemId = request.json.get('itemId')
    ctl = CartControl()
    res = ctl.getOneItemInfoInCart(userId, itemId)
    if res:
        return Response(json.dumps({'value': res}), status = 200)
    return "There has been an error"



"""
Incoming json requirement:
    userId: int
Response:
    a response class of Flask
        value: a list of tuple
"""
@app.route("/getallitemincart", methods=["GET"])
def getAllItemInfoInCart():
    userId = request.json.get('userId')
    ctl = CartControl()
    res = ctl.getAllItemInfoInCart(userId)
    if res:
        return Response(json.dumps({'value': res}), status = 200)
    return "There has been an error"



# Run the Flask application as a server
if __name__ == "__main__":
    DBctl = DatabaseControl()
    DBctl.CreateTable()
    app.run(port=Port)


