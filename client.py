import hashlib
import sys
from datetime import date, datetime, timedelta
import requests

#client function
def client(port):
    #add category
    catedic = {"name":"drink"}
    p = requests.post(url=f"http://127.0.0.1:{port}/addcategory", json=catedic)
    data = p.text
    print(data)

    #delete category
    # catedic = {"ID":1}
    # p = requests.delete(url=f"http://127.0.0.1:{port}/deletecategory", json=catedic)
    # data = p.text
    # print(data)

    # #add an item
    itemdic = {"sellerID":123,"name":"water", "category":"drink","quantity":1,"cur_price":10,"start_time":datetime.timestamp(datetime.now()),"end_time":datetime.timestamp(datetime(2019,11,10,10,5)),"buy_now":False,"buy_now_price":0,"shipping_cost":5,"description":"aawlsome"}
    print(itemdic) 
    p = requests.post(url=f"http://127.0.0.1:{port}/additem", json=itemdic)
    data = p.text
    print(data)
    #print(p.status_code)

    # #update price
    # info = {"ID":1,"cur_price":100}
    # p = requests.put(url=f"http://127.0.0.1:{port}/updateprice", json=info)
    # data = p.text
    # print(data)    

    # #update status
    # info = {"ID":1,"status":False}
    # p = requests.put(url=f"http://127.0.0.1:{port}/updatestatus", json=info)
    # data = p.text
    # print(data)

    # #search by category
    # info = {"name":"drink"}
    # p = requests.put(url=f"http://127.0.0.1:{port}/searchbycategory", json=info)
    # data = p.text
    # print(data)    

if __name__ == "__main__":
    #python client.py
    port = 9000
    client(port)

    