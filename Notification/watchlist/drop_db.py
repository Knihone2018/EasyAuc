#!/usr/bin/python3

import pymongo

client = pymongo.MongoClient(host='localhost', port=27017)
client.drop_database("watchlist")
dbs = client.list_databases()
for db in dbs:
    print(db)