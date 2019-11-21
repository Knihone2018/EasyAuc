#!/usr/bin/python3

title = {
    'toSeller': 'Item you sell got bid',
    'toBider': 'A higher bid',
    'oneDayCountDown': 'Only one day left',
    'oneHourCountDown': 'Only one hour left',
    'watchlist': 'A new item added into your watchlist'
}

content = {
    'toSeller': """\
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
        """, 
    "toBider":"""\
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
            """,
    "oneDayCountDown": """\
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
            """,
    "oneHourCountDown": """\
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
            """,
    "watchlist": """\
            <html>
                <body>
                    <p>Hi!<br>
                    <br>
                    A new item has been added into your watchlist!<br>
                    Click <a href="{}">here</a> to have a look now!<br>
                    <br>
                    Thanks for using EasyAuc!
                    </p>
                </body>
            </html>
            """
}