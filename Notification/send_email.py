#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
import traceback
import pymongo


def getTitleAndContent(contentType):

    client = pymongo.MongoClient(host='localhost', port=27017)
    db = client.email_content
    titleList = db.eTitle
    contentList = db.eContent

    titleResult = titleList.find_one({'type': contentType})
    contentResult = contentList.find_one({'type': contentType})

    result = {'title': titleResult['title'], 'content': contentResult['content']}
    return result

def sendEmial(reciverAddress, contentType, auctionURL):

    sender = "easyAuc19@gmail.com"
    password = "orientEasyAuc"

    result = getTitleAndContent(contentType)
    title = result['title']
    content = result['content']

    try:
        msg = MIMEText(content.format(auctionURL), 'html')
        msg['From'] = formataddr(["EasyAuc", sender])
        msg['To'] = formataddr([reciverAddress, reciverAddress])
        msg['Subject'] = title

        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(sender, password)
        server.sendmail(sender, reciverAddress, msg.as_string())
        server.quit()
        return True
    except Exception:
        traceback.print_exc()
        print("Sending email failed!")
        return False
    

sendEmial("angbian16@gmail.com", "toSeller", "www.google.com")
sendEmial("angbian16@gmail.com", "toBider", "www.amazon.com")
sendEmial("angbian16@gmail.com", "oneDayCountDown", "www.uchicago.edu")
sendEmial("angbian16@gmail.com", "oneHourCountDown", "www.ebay.com")