import mysql.connector
from flask import Flask, request, jsonify, Response
import json
from datetime import datetime


class DatabaseControl:
    
    def CreateTable(self):
        self.CreateDatabase()
        self.Getdb()
        self.CreateCartTable()
        self.CreateAccountTable()
        self.CreateBoughtItemsTable()


    def Getdb(self):
        mydb = mysql.connector.connect(
          host="localhost",
          user="root",
          passwd="a1s2d3f4",
          database="USER"
        )
        self.db = mydb
        return mydb


    def CreateDatabase(self):
        mydb = mysql.connector.connect(
          host="localhost",
          user="root",
          passwd="a1s2d3f4"
        )
        mycursor = mydb.cursor()
        mycursor.execute("CREATE DATABASE IF NOT EXISTS USER")


    def CreateCartTable(self):
        self.db.cursor().execute("create table if not exists Cart (userId int, itemId int, quantity int, isBid int);")
        self.db.commit()


    def CreateAccountTable(self):
        self.db.cursor().execute("create table if not exists Account (\
                                        userId int auto_increment primary key,\
                                        email varchar(150) unique,\
                                        firstname varchar(255),\
                                        lastname varchar(255),\
                                        password varchar(300),\
                                        address varchar(1000),\
                                        zipcode int,\
                                        city varchar(100),\
                                        state varchar(50),\
                                        bankAccountNumber int,\
                                        isBlocked int default 0,\
                                        isDeleted int default 0,\
                                        isAdmin int default 0,\
                                        ratingSum int,\
                                        numOfRates int);")
        self.db.commit()


    def CreateBoughtItemsTable(self):
        self.db.cursor().execute("create table if not exists BoughtItems (userId int, itemId int, quantity int, checkOutTime datetime);")
        self.db.commit()


class AccountControl(DatabaseControl):

    def addAccount(self, email, firstname, lastname, password, address, zipcode, city, state, bankAccountNumber, isBlocked, isDeleted, isAdmin, ratingSum, numOfRates):
        db = self.Getdb()
        cursor = db.cursor()

        userId = self.getUserIdByEmail(email)
        # if we can find the user record
        if userId:
            # if the account is deleted
            isDeleted = self.checkDeleteByUserId(userId)
            if isDeleted:
                cursor.execute("update Account set isDeleted = 0 where userId = %s;", (int(userId),))
                db.commit()
                return userId

            # if the account is blocked
            isBlocked = self.checkBlockByUserId(userId)
            if isBlocked:
                return False

            # else, user already exists
            return False


        # else, insert
        sql = "insert into Account (email, firstname, lastname, password, address, zipcode, city, state, bankAccountNumber, isBlocked, isDeleted, isAdmin, ratingSum, numOfRates)\
                values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        cursor.execute(sql, (email, firstname, lastname, password, address, zipcode, city, state, bankAccountNumber, isBlocked, isDeleted, isAdmin, ratingSum, numOfRates))
        db.commit()
        # get userId
        res = self.getUserIdByEmail(email)
        return res


    def addRating(self, userId, rate):
        db = self.Getdb()
        cursor = db.cursor()
        cursor.execute("update Account set numOfRates = numOfRates + 1, ratingSum = ratingSum + %s where userId = %s;", (int(rate), int(userId)))
        cursor.commit()
        return True

    def getRating(self, userId):
        db = self.Getdb()
        cursor = db.cursor()
        cursor.execute("select ratingSum from Account where userId = %s;", (int(userId),))
        res0 = cursor.fetchone()
        cursor.execute("select numOfRates from Account where userId = %s;", (int(userId),))
        res1 = cursor.fetchone()
        if res0 and res1:
            return res0[0] * 1.0 / res1[0]
        return -1


    def getUserIdByEmail(self, email):
        db = self.Getdb()
        cursor = db.cursor()
        cursor.execute("select userId from Account where email = %s;", (email,))
        res = cursor.fetchone()
        if res:
            return res[0]
        return False


    def deleteAccount(self, userId):
        db = self.Getdb()
        cursor = db.cursor()
        isDeleted = self.checkDeleteByUserId(userId)
        if isDeleted:
            return False
        else:
            cursor.execute("update Account set isDeleted = 1 where userId = %s;", (int(userId),))
            db.commit()
            return userId
        return False


    def blockAccount(self, userId):
        db = self.Getdb()
        cursor = db.cursor()
        isBlocked = self.checkBlockByUserId(userId)
        if isBlocked:
            return "User Already Deleted"
        else:
            cursor.execute("update Account set isBlocked = 1 where userId = %s;", (int(userId),))
            db.commit()
            return True
        return False


    def checkDeleteByUserId(self, userId):
        try:
            db = self.Getdb()
            cursor = db.cursor(buffered = True)
            cursor.execute("select isDeleted from Account where userId = %s;", (int(userId),))
            res = cursor.fetchone()
            return res[0]
        except:
            return -1


    def checkBlockByUserId(self, userId):
        try:
            db = self.Getdb()
            cursor = db.cursor(buffered = True)
            cursor.execute("select isBlocked from Account where userId = %s;", (int(userId),))
            res = cursor.fetchone()
            return res[0]
        except:
            return -1


    def checkIsAdminByUserId(self, userId):
        try:
            db = self.Getdb()
            cursor = db.cursor(buffered = True)
            cursor.execute("select isAdmin from Account where userId = %s;", (int(userId),))
            res = cursor.fetchone()
            return res[0]
        except:
            return -1


    def getUserEmailbyUserId(self, userId):
        db = self.Getdb()
        cursor = db.cursor(buffered = True)
        cursor.execute("select email from Account where userId = %s;", (int(userId),))
        res = cursor.fetchone()
        if res:
            return res[0]
        return False



    def setEmail(self, userId, newEmail):
        try:
            db = self.Getdb()
            mycursor = db.cursor()
            mycursor.execute("update Account set email = %s where userId = %s;", (newEmail, int(userId)))
            db.commit()
            return True
        except:
            return False


    def getUserFirstname(self, userId):
        db = self.Getdb()
        cursor = db.cursor(buffered = True)
        cursor.execute("select firstname from Account where userId = %s;", (int(userId),))
        res = cursor.fetchone()
        if res:
            return res[0]
        return False


    def setFirstname(self, userId, newStr):
        try:
            db = self.Getdb()
            mycursor = db.cursor()
            mycursor.execute("update Account set firstname = %s where userId = %s;", (newStr, int(userId)))
            db.commit()
            return True
        except:
            return False


    def getUserLastname(self, userId):
        db = self.Getdb()
        cursor = db.cursor(buffered = True)
        cursor.execute("select lastname from Account where userId = %s;", (int(userId),))
        res = cursor.fetchone()
        if res:
            return res[0]
        return False


    def setLastname(self, userId, newStr):
        try:
            db = self.Getdb()
            mycursor = db.cursor()
            mycursor.execute("update Account set lastname = %s where userId = %s;", (newStr, int(userId)))
            db.commit()
            return True
        except:
            return False

    def checkSignin(self, email, pwd):
        db = self.Getdb()
        mycursor = db.cursor()
        cursor.execute("select password from Account where email = %s;", (email,))
        password = cursor.fetchone()
        cursor.execute("select userId from Account where email = %s;", (email,))
        userId = cursor.fetchone()
        if password and userId:
            if password == pwd:
                return {'success': True, 'userId': userId}
            else:
                return {'success': False, 'userId': userId}
        return False


    def getUserPassword(self, userId):
        db = self.Getdb()
        cursor = db.cursor(buffered = True)
        cursor.execute("select password from Account where userId = %s;", (int(userId),))
        res = cursor.fetchone()
        if res:
            return res[0]
        return False


    def setPassword(self, userId, newStr):
        try:
            db = self.Getdb()
            mycursor = db.cursor()
            mycursor.execute("update Account set password = %s where userId = %s;", (newStr, int(userId)))
            db.commit()
            return True
        except:
            return False

    def getUserAddress(self, userId):
        db = self.Getdb()
        cursor = db.cursor(buffered = True)
        cursor.execute("select address from Account where userId = %s;", (int(userId),))
        res = cursor.fetchone()
        if res:
            return res[0]
        return False


    def setAddress(self, userId, newStr):
        try:
            db = self.Getdb()
            mycursor = db.cursor()
            mycursor.execute("update Account set address = %s where userId = %s;", (newStr, int(userId)))
            db.commit()
            return True
        except:
            return False


    def getUserZipcode(self, userId):
        db = self.Getdb()
        cursor = db.cursor(buffered = True)
        cursor.execute("select zipcode from Account where userId = %s;", (int(userId),))
        res = cursor.fetchone()
        if res:
            return res[0]
        return False

    def setZipcode(self, userId, newNum):
        try:
            db = self.Getdb()
            mycursor = db.cursor()
            mycursor.execute("update Account set zipcode = %s where userId = %s;", (int(newNum), int(userId)))
            db.commit()
            return True
        except:
            return False


    def getUserCity(self, userId):
        db = self.Getdb()
        cursor = db.cursor(buffered = True)
        cursor.execute("select city from Account where userId = %s;", (int(userId),))
        res = cursor.fetchone()
        if res:
            return res[0]
        return False


    def setCity(self, userId, newStr):
        try:
            db = self.Getdb()
            mycursor = db.cursor()
            mycursor.execute("update Account set city = %s where userId = %s;", (newStr, int(userId)))
            db.commit()
            return True
        except:
            return False


    def getUserState(self, userId):
        db = self.Getdb()
        cursor = db.cursor(buffered = True)
        cursor.execute("select state from Account where userId = %s;", (int(userId),))
        res = cursor.fetchone()
        if res:
            return res[0]
        return False


    def setState(self, userId, newStr):
        try:
            db = self.Getdb()
            mycursor = db.cursor()
            mycursor.execute("update Account set state = %s where userId = %s;", (newStr, int(userId)))
            db.commit()
            return True
        except:
            return False


    def getUserBankAccNum(self, userId):
        try:
            db = self.Getdb()
            cursor = db.cursor(buffered = True)
            cursor.execute("select bankAccountNumber from Account where userId = %s;", (int(userId),))
            res = cursor.fetchone()
            if res:
                return res[0]
            return False
        except:
            return False


    def setBankAccNum(self, userId, newNum):
        try:
            db = self.Getdb()
            mycursor = db.cursor()
            mycursor.execute("update Account set bankAccountNumber = %s where userId = %s;", (int(newNum), int(userId)))
            db.commit()
            return True
        except:
            return False

    def dropTable(self):
        db = self.Getdb()
        cursor = db.cursor(buffered = True)
        cursor.execute("drop table if exists Account cascade;")
        db.commit()
        return True




class CartControl(DatabaseControl):

    def addToCart(self, userId, itemId, addQuantity, isBid):
        try:
            db = self.Getdb()
            mycursor = db.cursor()

            res = self.getOneItemInfoInCart(userId, itemId)
            if res:
                mycursor.execute("update Cart set quantity = quantity + %s where userId = %s and itemId = %s;", (int(addQuantity), int(userId), int(itemId)))
            else:
                mycursor.execute("insert into Cart (userId, itemId, quantity, isBid) values (%s, %s, %s, %s);", (int(userId), int(itemId), int(addQuantity), int(isBid)))
            db.commit()
            return True
        except:
            return False


    def deleteFromCart(self, userId, itemId, deleteQuantity):
        try:
            db = self.Getdb()
            mycursor = db.cursor()
            if self.checkItemIsBid(userId, itemId):
                return "Cannot delete a bid item"

            res = self.getOneItemInfoInCart(userId, itemId)
            if res:
                mycursor.execute("update Cart set quantity = quantity - %s where userId = %s and itemId = %s;", (int(deleteQuantity), int(userId), int(itemId)))
                db.commit()
                mycursor.execute("delete from Cart where quantity = 0;")
                db.commit()
                return True
            else:
                return False
        except:
            return False


    # after pay everything
    def emptyCart(self, userId):
        try:
            db = self.Getdb()
            mycursor = db.cursor()
            mycursor.execute("delete from Cart where userId = %s;", (int(userId),))
            db.commit()
            return True
        except:
            return False



    def checkItemIsBid(self, userId, itemId):
        try:
            db = self.Getdb()
            cursor = db.cursor(buffered = True)

            cursor.execute("select isBid from Cart where userId = %s and itemId = %s;", (int(userId), int(itemId)))
            res = cursor.fetchone()
            return res
        except:
            return -1


    def getOneItemInfoInCart(self, userId, itemId):
        try:
            db = self.Getdb()
            cursor = db.cursor(buffered = True)

            cursor.execute("select itemId, quantity, isBid from Cart where userId = %s and itemId = %s;", (int(userId), int(itemId)))
            res = cursor.fetchone()
            if res:
                return res
            return False
        except:
            return False


    def getAllItemInfoInCart(self, userId):
        try:
            db = self.Getdb()
            cursor = db.cursor(buffered = True)

            cursor.execute("select itemId, quantity, isBid from Cart where userId = %s;", (int(userId),))
            res = cursor.fetchall()
            if res:
                return res
            return False
        except:
            return False

    def dropTable(self):
        db = self.Getdb()
        cursor = db.cursor(buffered = True)
        cursor.execute("drop table if exists Cart cascade;")
        db.commit()
        return True


class BoughtItemsControl(DatabaseControl):

    def dropTable(self):
        db = self.Getdb()
        cursor = db.cursor(buffered = True)
        cursor.execute("drop table if exists BoughtItems cascade;")
        db.commit()
        return True


    def addItemToBoughtList(self, userId, itemId, quantity):
        db = self.Getdb()
        cursor = db.cursor(buffered = True)
        cursor.execute("insert into BoughtItems (userId, itemId, quantity, checkOutTime) values (%s, %s, %s, %s);", (int(userId), int(itemId), int(quantity), datetime.now()))
        db.commit()
        return True


    def getAllBoughtItems(self, userId):
        try:
            db = self.Getdb()
            cursor = db.cursor(buffered = True)

            cursor.execute("select itemId, quantity, checkOutTime from BoughtItems where userId = %s;", (int(userId),))
            res = cursor.fetchall()
            if res:
                return res
            return False
        except:
            return False




    