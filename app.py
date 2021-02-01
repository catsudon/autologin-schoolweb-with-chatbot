import os
from flask import Flask,request
import json
import requests
import selenium
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import time
from config import *
import pandas as pd

app = Flask(__name__)

# global student
# global pw
global op
op = webdriver.ChromeOptions()
op.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
op.add_argument("--headless")
op.add_argument("--no-sandbox")
op.add_argument("--disable-dev-sh-usage")
driver = webdriver.Chrome(executable_path = os.environ.get("CHROMEDRIVER_PATH"), chrome_options=op)


@app.route("/",methods=['POST','GET'])
def webhook():
    if request.method == 'POST':
        payload = request.json
        reply_token = payload['events'][0]['replyToken']
        url = payload['events'][0]['message']['text']
        # if url[0:4]not=="http": #check the code if its link or not
        #     flask.abort(404)
        returnstatus = login(url)
        returnstatus = checksts(len(returnstatus))
        reply(reply_token,returnstatus)
        checkfortherest(url,)

        return 200
    else:
        return "Hello World!"

def login(url):
    driver.get(url)
    form = driver.find_elements_by_class_name("form-control")
    form[0].send_keys("48853")
    form[1].send_keys("000000")

    button = driver.find_element_by_name("submit")
    button.click()
    time.sleep(1)
    return(driver.page_source.encode("utf-8"))

def reply(token,returnstatus):
    print(returnstatus)
    LINE_API = 'https://api.line.me/v2/bot/message/reply'
    Authorization = 'Bearer {}'.format(access_token)
    print(Authorization)
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization': Authorization
    }

    data = {
        "replyToken":token,
        "messages":[{
      "type": "text",
      "text": returnstatus
}]
    }
    data = json.dumps(data)
    r = requests.post(LINE_API, headers=headers, data=data) 
    return 200


def checkfortherest(url):
    sts = []
    for i in student:
        url = 'https://notify-api.line.me/api/notify'
        headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer ' + line_notify_token}
        status = loginfortherest(url,i)
        status = checksts(len(status))
        msg = student[i] + " - " + status
        r = requests.post(url, headers=headers, data = {'message':msg})
    return 200

def loginfortherest(url,i):
    driver.get(url)
    form = driver.find_elements_by_class_name("form-control")
    form[0].send_keys(studedt[i])
    form[1].send_keys(pw[i])
    button = driver.find_element_by_name("submit")
    button.click()
    time.sleep(1)
    return(driver.page_source.encode("utf-8"))

def checksts(num):
    if num==70593:
        returnstatus = "ขณะนี้ยังไม่มีอะไรให้เช็ค"
    elif num==73391:
        returnstatus = "คุณได้เช็คชื่อวิชานี้ไปแล้ว"
    elif num==40812:
        returnstatus = "ไม่สามารถล็อคอินได้"
    else:
        # returnstatus = "เช็คได้ไหมกูไม่รู้ กูยังอยู่ในช่วงพัฒนา"
        returnstatus = len(returnstatus)
    return returnstatus
