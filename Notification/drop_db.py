#!/usr/bin/python3

import pymongo

client = pymongo.MongoClient(host='localhost', port=27017)
# myClient.drop_database('email_content')
dbs = client.list_databases()
for db in dbs:
    print(db)