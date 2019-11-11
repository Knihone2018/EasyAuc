#!/usr/bin/python3

import pymongo

client = pymongo.MongoClient(host='localhost', port=27017)
db = client.email_content

titleList = db.eTitle
contentList = db.eContent

toSellerTitle = {
    'type': 'toSeller',
    'title': 'Item you sell got bid'
}
toBiderTitle = {
    'type': 'toBider',
    'title': 'A higher bid'
}
oneDayCountDownTitle = {
    'type': 'oneDayCountDown',
    'title': 'Only one day left'
}
oneHourCountDownTitle = {
    'type': 'oneHourCountDown',
    'title': 'Only one hour left'
}

toSellerContent = {
    'type': 'toSeller',
    'content': """\
        <html>
            <body>
                <p>Hi!<br>
                <br>
                Someone has bid on the item your are selling!<br>
                Click <a href="{}">here</a> to check details!<br>
                <br>
                Thanks for using EasyAuc!
                </p>
            </body>
        </html>
        """
}
toBiderContent = {
    'type': "toBider",
    'content': """\
            <html>
                <body>
                    <p>Hi!<br>
                    <br>
                    Someone has placed a higher bid on the item you bid!<br>
                    Check detail and bid higher <a href="{}">here</a>.<br>
                    <br>
                    Thanks for using EasyAuc!
                    </p>
                </body>
            </html>
            """
}
oneDayCountDownContent = {
    'type': "oneDayCountDown",
    'content': """\
            <html>
                <body>
                    <p>Hi!<br>
                    <br>
                    Only one day left for your item!<br>
                    Click <a href="{}">here</a> to check details!<br>
                    <br>
                    Thanks for using EasyAuc!
                    </p>
                </body>
            </html>
            """
}
oneHourCountDownContent = {
    'type': "oneHourCountDown",
    'content': """\
            <html>
                <body>
                    <p>Hi!<br>
                    <br>
                    Only one hour left for your item!<br>
                    Click <a href="{}">here</a> to check details!<br>
                    <br>
                    Thanks for using EasyAuc!
                    </p>
                </body>
            </html>
            """
}

titleList.insert_many([toSellerTitle, toBiderTitle, oneDayCountDownTitle, oneHourCountDownTitle])
contentList.insert_many([toSellerContent, toBiderContent, oneDayCountDownContent, oneHourCountDownContent])