import mysql.connector
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import json
from datetime import datetime



mydb = mysql.connector.connect(
          host="localhost",
          user="root",
          passwd="a1s2d3f4"
        )
mycursor = mydb.cursor()
mycursor.execute("CREATE DATABASE IF NOT EXISTS USER")


db = mysql.connector.connect(
          host="localhost",
          user="root",
          passwd="a1s2d3f4",
          database="USER"
        )

db.cursor().execute("create table if not exists Account (\
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
db.commit()

db.cursor().execute("insert into Account (email, password, isAdmin) values ('admin@easyauc.com','123', 1);")
db.commit()

