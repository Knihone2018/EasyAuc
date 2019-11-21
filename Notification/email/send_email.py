#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
import traceback
import pika
import email_content
import json

def sendEmail(reciverAddress, contentType, auctionURL):

    sender = "easyAuc19@gmail.com"
    password = "orientEasyAuc"

    title = email_content.title[contentType]
    content = email_content.content[contentType]

    try:
        msg = MIMEText(content.format(auctionURL), 'html')
        msg['From'] = formataddr(["EasyAuc", sender])
        msg['To'] = "Customers"
        msg['Subject'] = title

        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(sender, password)
        server.sendmail(sender, reciverAddress.split(','), msg.as_string())
        server.quit()
        return True
    except Exception:
        traceback.print_exc()
        print("Sending email failed!")
        return False

def getUserEmail(user_id):
    return "angbian16@gmail.com,angbian@uchicago.edu,ang.bian96@gmail.com"

def callback(ch, method, properties, body):
    emailInfo = json.loads(body)
    print(emailInfo)
    user_email = getUserEmail(emailInfo["user_id"])
    sendEmail(user_email, emailInfo["type"], emailInfo['url'])


connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='172.17.0.2'))
channel = connection.channel()

channel.queue_declare(queue='email')
channel.basic_consume(
    queue='email', on_message_callback=callback, auto_ack=True)
print("Service starts!")
channel.start_consuming()

# sendEmial("angbian16@gmail.com,angbian@uchicago.edu,ang.bian96@gmail.com", "toSeller", "www.google.com")
