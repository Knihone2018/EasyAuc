#!/usr/bin/env python3

from flask import Flask, jsonify, request
import pymongo
import uuid
# from getItemDetail import GetItemDetail

watchlist = Flask(__name__)

dbClient = pymongo.MongoClient(host='localhost', port=27017)
watchlist_db = dbClient["watchlist"]
itemCollection = watchlist_db["items"]
paraCollection = watchlist_db["parameters"]
# getItemDetail = GetItemDetail()

# Parameters
def getItemNames(user_id):
    results = paraCollection.find({'user_id': user_id})
    names = []
    for result in results:
        names.append(result['item_name'])
    return names

@watchlist.route('/parameters', methods=['POST'])
def insertParameter():
    if not request.json:
        return jsonify({'err': 'Invalid json format'})
    else:
        input = request.json
        if input['item_name'] in getItemNames(input['user_id']):
            return jsonify({'success': True})
        para = {'user_id': input['user_id'],
        'item_name': input['item_name'], 'category': input['category'], 
        'min_price': input['min_price'], 'max_price': input['max_price']}
        paraCollection.insert_one(para)
        return jsonify({'success': True})

@watchlist.route('/parameters/<user_id>', methods=['GET'])
def getParameter(user_id):
    results = paraCollection.find({'user_id': user_id})
    paras = []
    for result in results:
        para = {'user_id': result['user_id'],
        'item_name': result['item_name'], 'category': result['category'], 
        'min_price': result['min_price'], 'max_price': result['max_price']}
        paras.append(para)
    return jsonify({'paras': paras})

@watchlist.route('/parameters', methods=['PUT'])
def updateParameter():
    if not request.json:
        return jsonify({'err': 'Invalid json format'})
    else:
        input = request.json
        condition = {'user_id': input['user_id'], 'item_name': input['item_name']}
        para = {}
        para['min_price'] = input['min_price']
        para['max_price'] = input['max_price']
        paraCollection.update_one(condition, {'$set': para})
        return jsonify({'success': True})

@watchlist.route('/parameters', methods=['DELETE'])
def deleteParameter():
    if not request.json:
        return jsonify({'err': 'Invalid json format'})
    else:
        input = request.json
        paraCollection.remove({'user_id': input['user_id'], 'item_name': input['item_name']})
        return jsonify({'success': True})


# Watchlist
def getItemIDs(user_id):
    results = itemCollection.find({'user_id': user_id})
    itemIDs = []
    for result in results:
        itemIDs.append(result['item_id'])
    return itemIDs

@watchlist.route('/watchlist', methods=['POST'])
def insertItem():
    if not request.json:
        return jsonify({'err': 'Invalid json format'})
    else:
        input = request.json
        if input['item_id'] in getItemIDs(input['user_id']):
            return jsonify({'success': True})
        item = {
            "user_id": input['user_id'],
            "item_id": input['item_id']
        }
        itemCollection.insert_one(item)
        return jsonify({'success': True})

# TODO: request items info using item ID
@watchlist.route('/watchlist/<user_id>', methods=['GET'])
def getItems(user_id):
    # itemIDs = ",".join(getItemIDs(user_id))
    # items = getItemDetail.call(itemIDs)
    # print(items)
    # return items
    itemIDs = getItemIDs(user_id)
    return jsonify({'items': itemIDs})

@watchlist.route('/watchlist', methods=['DELETE'])
def deleteItems():
    if not request.json:
        return jsonify({'err': 'Invalid json format'})
    else:
        input = request.json
        itemCollection.remove({'user_id': input['user_id'], 'item_id': input['item_id']})
        return jsonify({'success': True})

if __name__=='__main__':
    watchlist.run(debug=True, host='0.0.0.0')