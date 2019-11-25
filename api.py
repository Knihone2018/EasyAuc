from flask import Flask, request, Response, jsonify
from flasgger import Swagger
from user import *



app = Flask(__name__)
Swagger(app)
Port = 5672



####################################################
# restful apis
####################################################

@app.route("/checkoutcart", methods=["GET"])
def checkoutCart():
    userId = request.json.get('userId')
    cart = CartControl()
    history = BoughtItemsControl()
    items = cart.getAllItemInfoInCart(userId)
    for row in items:
        try:
            history.addItemToBoughtList(userId, row[0], row[1])
        except:
            return Response(json.dumps({'success': False}), status = 500, mimetype='application/json')
    emptyRes = cart.emptyCart(userId)
    if emptyRes:
        return Response(json.dumps({'success': True}), status = 200, mimetype='application/json')
    return Response(json.dumps({'success': False}), status = 500, mimetype='application/json')


######################
# Getters for Account Database
######################



@app.route("/myaccount.html?id=<userId>", methods=["GET"])
def getAllUserInfo(userId):
    try:
        ctl = AccountControl()
        email = ctl.getUserEmailbyUserId(userId)
        firstname = ctl.getUserFirstname(userId)
        lastname = ctl.getUserLastname(userId)
        pwd = ctl.getUserPassword(userId)
        address = ctl.getUserAddress(userId)
        zipcode = ctl.getUserZipcode(userId)
        city = ctl.getUserCity(userId)
        state = ctl.getUserState(userId)
        bankAcc = ctl.getUserBankAccNum(userId)
        rating = ctl.getRating(userId)
        isBlocked = ctl.checkBlockByUserId(userId)
        isDeleted = ctl.checkDeleteByUserId(userId)
        isAdmin = ctl.checkIsAdminByUserId(userId)
        return Response(json.dumps({'success': True, 'email':email, 'firstname':firstname, 'lastname':lastname, 'password':pwd, 
            'address':address, 'zipcode':zipcode, 'city':city, 'state':state, 'bankAccount':bankAcc, 'rating':rating,
            'isBlocked':isBlocked, 'isDeleted':isDeleted, 'isAdmin':isAdmin}), status = 200, mimetype='application/json')
    except:
        return Response(json.dumps({'success': False}), status = 500, mimetype='application/json')



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
        return Response(json.dumps({'success': True, 'value': res}), status = 200, mimetype='application/json')
    return Response(json.dumps({'success': False}), status = 500, mimetype='application/json')


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
        return Response(json.dumps({'success': True, 'value': res}), status = 200, mimetype='application/json')
    return Response(json.dumps({'success': False}), status = 500, mimetype='application/json')


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
        return Response(json.dumps({'success': True, 'value': res}), status = 200, mimetype='application/json')
    return Response(json.dumps({'success': False}), status = 500, mimetype='application/json')


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
        return Response(json.dumps({'success': True, 'value': res}), status = 200, mimetype='application/json')
    return Response(json.dumps({'success': False}), status = 500, mimetype='application/json')


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
        return Response(json.dumps({'success': True, 'value': res}), status = 200, mimetype='application/json')
    return Response(json.dumps({'success': False}), status = 500, mimetype='application/json')


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
        return Response(json.dumps({'success': True, 'password': res}), status = 200, mimetype='application/json')
    return Response(json.dumps({'success': False}), status = 500, mimetype='application/json')


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
        return Response(json.dumps({'success': True, 'value': res}), status = 200, mimetype='application/json')
    return Response(json.dumps({'success': False}), status = 500, mimetype='application/json')



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
        return Response(json.dumps({'success': True, 'value': res}), status = 200, mimetype='application/json')
    return Response(json.dumps({'success': False}), status = 500, mimetype='application/json')


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
        return Response(json.dumps({'success': True, 'value': res}), status = 200, mimetype='application/json')
    return Response(json.dumps({'success': False}), status = 500, mimetype='application/json')



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
        return Response(json.dumps({'success': True, 'value': res}), status = 200, mimetype='application/json')
    return Response(json.dumps({'success': False}), status = 500, mimetype='application/json')


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
        return Response(json.dumps({'success': True, 'value': res}), status = 200, mimetype='application/json')
    return Response(json.dumps({'success': False}), status = 500, mimetype='application/json')


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
        return Response(json.dumps({'success': True, 'userId': res}), status = 200, mimetype='application/json')
    return Response(json.dumps({'success': False}), status = 500, mimetype='application/json')


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
        return Response(json.dumps({'success': True, 'userId': res}), status = 200, mimetype='application/json')
    return Response(json.dumps({'success': False}), status = 500, mimetype='application/json')



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
        return Response(json.dumps({'success': True, 'userId': res}), status = 200, mimetype='application/json')
    return Response(json.dumps({'success': False}), status = 500, mimetype='application/json')



"""
Incoming json requirement:
    sellerId: int
    rate: int
Response:
    a response class of Flask
        userId: int
"""
@app.route("/addsellerrate", methods=["POST"])
def addOneSellerRating():
    userId = request.json.get('sellerId')
    newNum = request.json.get('rate')
    ctl = AccountControl()
    res = ctl.addRating(userId, newNum)
    if res:
        return Response(json.dumps({'success': True, 'sellerId': userId}), status = 200, mimetype='application/json')
    return Response(json.dumps({'success': False}), status = 500, mimetype='application/json')



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
        return Response(json.dumps({'success': True, 'userId': userId}), status = 200, mimetype='application/json')
    return Response(json.dumps({'success': False}), status = 500, mimetype='application/json')



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
        return Response(json.dumps({'success': True, 'userId': userId}), status = 200, mimetype='application/json')
    return Response(json.dumps({'success': False}), status = 500, mimetype='application/json')



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
        return Response(json.dumps({'success': True, 'userId': userId}), status = 200, mimetype='application/json')
    return Response(json.dumps({'success': False}), status = 500, mimetype='application/json')


"""
Incoming json requirement:
    userId: int
    password: string
Response:
    a response class of Flask
        userId: int
"""
@app.route("/setpassword", methods=["POST"])
def setPassword():
    userId = request.json.get('userId')
    newStr = request.json.get('password')
    ctl = AccountControl()
    res = ctl.setPassword(userId, newStr)
    if res:
        return Response(json.dumps({'success': True, 'userId': userId}), status = 200, mimetype='application/json')
    return Response(json.dumps({'success': False}), status = 500, mimetype='application/json')


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
        return Response(json.dumps({'success': True, 'userId': userId}), status = 200, mimetype='application/json')
    return Response(json.dumps({'success': False}), status = 500, mimetype='application/json')


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
        return Response(json.dumps({'success': True, 'userId': userId}), status = 200, mimetype='application/json')
    return Response(json.dumps({'success': False}), status = 500, mimetype='application/json')


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
        return Response(json.dumps({'success': True, 'userId': userId}), status = 200, mimetype='application/json')
    return Response(json.dumps({'success': False}), status = 500, mimetype='application/json')



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
        return Response(json.dumps({'success': True, 'userId': userId}), status = 200, mimetype='application/json')
    return Response(json.dumps({'success': False}), status = 500, mimetype='application/json')



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
        return Response(json.dumps({'success': True, 'userId': userId}), status = 200, mimetype='application/json')
    return Response(json.dumps({'success': False}), status = 500, mimetype='application/json')





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
        return Response(json.dumps({'success': True, 'userId': userId}), status = 200, mimetype='application/json')
    return Response(json.dumps({'success': False}), status = 500, mimetype='application/json')



"""
Incoming json requirement:
    userId: int
    itemId: int
    deleteQuantity: int
Response:
    a response class of Flask
        userId: int
"""
@app.route("/deleteitemfromcart", methods=["POST"])
def deleteItemFromCart():
    userId = request.json.get('userId')
    itemId = request.json.get('itemId')
    deleteQuantity = request.json.get('deleteQuantity')
    ctl = CartControl()
    if ctl.checkItemIsBid(userId, itemId) == 1:
        return "Cannot delete an item won from a bid"
    res = ctl.deleteFromCart(userId, itemId, deleteQuantity)
    if res:
        return Response(json.dumps({'success': True, 'userId': userId}), status = 200, mimetype='application/json')
    return Response(json.dumps({'success': False}), status = 500, mimetype='application/json')



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
    # update the quantity to item microservice
    res = ctl.emptyCart(userId)
    if res:
        ## need to call restful api in Item to update quantity!
        return Response(json.dumps({'success': True, 'userId': userId}), status = 200, mimetype='application/json')
    return Response(json.dumps({'success': False}), status = 500, mimetype='application/json')




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
        return Response(json.dumps({'success': True, 'value': res}), status = 200, mimetype='application/json')
    return Response(json.dumps({'success': False}), status = 500, mimetype='application/json')



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
        return Response(json.dumps({'success': True, 'value': res}), status = 200, mimetype='application/json')
    return Response(json.dumps({'success': False}), status = 500, mimetype='application/json')




@app.route("/cart.html?id=<userId>", methods=["GET"])
def getAllItemInfoInCart(userId):
    ctl = CartControl()
    res = ctl.getAllItemInfoInCart(userId)
    result = []
    if res:
        for i in xrange(len(res)):
            # itemId, quantity, isBid
            try:
                resItem = requests.get(url="http://localhost:9000/getitembyid", json = {"ID": res[i][0]})
                itemInfo = resItem.json()
                sellerID = itemInfo['sellerID']
                name = itemInfo['name']
                category = itemInfo['category']
                cur_price = itemInfo['cur_price']
                price_step = itemInfo['price_step']
                start_time = itemInfo['start_time']
                end_time = itemInfo['end_time']
                flag = itemInfo['flag']
                buy_now = itemInfo['buy_now']
                buy_now_price = itemInfo['buy_now_price']
                shipping_cost = itemInfo['shipping_cost']
                description = itemInfo['description']
                url = itemInfo['url']
                status = itemInfo['status']
                photo = itemInfo['photo']
                result.append({'itemId':res[i][0], 'quantity':res[i][1], 'isBid': res[i][2], 'sellerID':sellerID, 
                    'name':name, 'category':category, 'cur_price':cur_price, 'price_step':price_step,
                    'start_time':start_time, 'end_time':end_time, 'flag':flag, 'buy_now':buy_now, 'buy_now_price':buy_now_price,
                    'shipping_cost':shipping_cost, 'description':description, 'url':url, 'status':status, 'photo':photo, 'success': True})
            except:
                result.append({'itemId': res[i][0], 'quantity':res[i][1], 'isBid': res[i][2], 'success': False})
        return Response(json.dumps({'success': True, 'items': result}), status = 200, mimetype='application/json')
    return Response(json.dumps({'success': False}), status = 500, mimetype='application/json')



######################
# Getters for BoughtItems Database
######################


@app.route("/history.html?id=<userId>", methods=["GET"])
def getAllBoughtItems(userId):
    ctl = BoughtItemsControl()
    res = ctl.getAllBoughtItems(userId)
    result = []
    if res:
        for i in xrange(len(res)):
            # itemId, quantity, checkOutTime
            try:
                resItem = requests.get(url="http://localhost:9000/getitembyid", json = {"ID": res[i][0]})
                itemInfo = resItem.json()
                sellerID = itemInfo['sellerID']
                name = itemInfo['name']
                category = itemInfo['category']
                cur_price = itemInfo['cur_price']
                price_step = itemInfo['price_step']
                start_time = itemInfo['start_time']
                end_time = itemInfo['end_time']
                flag = itemInfo['flag']
                buy_now = itemInfo['buy_now']
                buy_now_price = itemInfo['buy_now_price']
                shipping_cost = itemInfo['shipping_cost']
                description = itemInfo['description']
                url = itemInfo['url']
                status = itemInfo['status']
                photo = itemInfo['photo']
                result.append({'itemId':res[i][0], 'quantity':res[i][1], 'checkOutTime': res[i][2].strftime("%m/%d/%Y, %H:%M:%S")
                    , 'sellerID':sellerID, 'name':name, 'category':category, 'cur_price':cur_price, 'price_step':price_step,
                    'start_time':start_time, 'end_time':end_time, 'flag':flag, 'buy_now':buy_now, 'buy_now_price':buy_now_price,
                    'shipping_cost':shipping_cost, 'description':description, 'url':url, 'status':status, 'photo':photo, 'success': True})
            except:
                result.append({'success': False, 'itemId':res[i][0], 'quantity':res[i][1], 'checkOutTime': res[i][2].strftime("%m/%d/%Y, %H:%M:%S")})
        return Response(json.dumps({'success': True, 'items': result}), status = 200, mimetype='application/json')
    return Response(json.dumps({'success': False}), status = 500, mimetype='application/json')



######################
# Setters for BoughtItems Database
######################


"""
Incoming json requirement:
    userId: int
    value: [(itemId1, quantity1), (itemId2, quantity2), ... ]
Response:
    a response class of Flask
        value: a list of tuple
"""
@app.route("/additemstoboughtlist", methods=["POST"])
def addItemToBoughtList():
    userId = request.json.get('userId')
    val = request.json.get('value')
    ctl = BoughtItemsControl()
    for pair in val:
        res = ctl.addItemToBoughtList(userId, pair[0], pair[1])
        if not res:
            return Response(json.dumps({'success': False}), status = 500, mimetype='application/json')
    return Response(json.dumps({'success': True, 'userId': userId, "value": val}), status = 200, mimetype='application/json')


@app.route("/droptable/<tableName>", methods=["POST"])
def dropTable(tableName):
    if (tableName.strip()).lower() == "cart":
        ctl = CartControl()
    elif (tableName.strip()).lower() == "boughtitems":
        ctl = BoughtItemsControl()
    elif (tableName.strip()).lower() == "account":
        ctl = AccountControl()
    res = ctl.dropTable()
    if res:
        return Response(json.dumps({'success': True, 'success': res}), status = 200, mimetype='application/json')
    return Response(json.dumps({'success': False}), status = 500, mimetype='application/json')



# Run the Flask application as a server
if __name__ == "__main__":
    DBctl = DatabaseControl()
    DBctl.CreateTable()
    app.run(port=Port)


