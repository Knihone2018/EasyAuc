EasyAuc Notification

Implement email function and save the title and content of frequently used email type in MongoDB.


Restful Api: (implemented in watchlist.py)

User parameter part:
Add new parameter:
  request: 
    function: post
    url: /parameters
    Content-Type: application/json
    value: {
              "user_id": "123",
              "item_name": "MacBookPro",
              "category": "computer",
              "min_price": "100",
              "max_price": "1000"
            }
  return:
    {'success': True}
Get parameter:
  request:
    function: get
    url: /parameters/<user_id>
  return:
    {
      "paras": [
        {
          "category": "tablet",
          "item_name": "ipad",
          "max_price": "1000",
          "min_price": "100",
          "user_id": "999"
        }
      ]
    }
Update parameters:
  request:
    function: put
    url: /parameters
    Content-Type: application/json
    value: {
            "user_id": "123",
            "item_name": "MacBookPro",
            "min_price": "500",
            "max_price": "2000"
            }
  return:
    {'success': True}
Remove parameters:
  request:
    function: delete
    url: /parameters
    Content-Type: application/json
    value: {
              "user_id": "123",
              "item_name": "MacBookPro"
            }
  return:
    {'success': True}
    
    
 Watchlist part:
    Add to watchlist:
      request:
          function: post
          url: /watchlist
          Content-Type: application/json
          value:
            {
              "user_id": "123",
              "item_id": "12345"
            }
      return:
        {'success': True}
    Get watchlist:
        request:
          function: get
          url: /watchlist/<user_id>
        return:
          {
            "items": [
              "1234"
            ]
          }
    Remove item from watchlist:
        request:
          function: Delete
          url: /watchlist
          Content-Type: application/json
          value: 
          {
            "user_id": "123",
            "item_id": "12345"
          }
        return:
          {'success': True}
          
          
      
