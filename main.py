# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import random
# import pyowm  # import Python Open Weather Map to our project.
# from pyowm import OWM
import serial.tools.list_ports
import time
import sys
import requests
import json
import  Storage as STO
# from Adafruit_IO import MQTTClient

AIO_FEED_ID = ["multi-projct.button", "multi-projct.sound"]
AIO_USERNAME = "kinggiaan"
AIO_KEY = "aio_oyFJ6970b4VKFcRDqBkU3Y7gkTse"


def getPort():
    ports = serial.tools.list_ports.comports()
    N = len(ports)
    commPort = "None"
    for i in range(0, N):
        port = ports[i]
        strPort = str(port)
        if "USB Serial Device" in strPort:
            splitPort = strPort.split(" ")
            commPort = (splitPort[0])
            print(commPort)
    return commPort

isMicrobitConnected = False
if getPort() != "None":
    ser = serial.Serial( port=getPort(), baudrate=115200)
    isMicrobitConnected = True



# ser = serial.Serial(port=getPort(), baudrate=115200)

mess = ""
def processData(data):
    data = data.replace("!", "")
    data = data.replace("#", "")
    splitData = data.split(":")
    print(splitData)
    if splitData[0] == "BUTTON": #de nha sp ra va relay nhay on off on
        # r = requests.get('https://thay-tam.herokuapp.com/api/v1/ping')
        # print('Gui request thanh cong')
        # print(r)
        # print(r.json())
        Machine_ReleasePro(2)
        #ser.write(("BUTTON" + "#").encode())

    # if splitData[0] == "HUMI":
        # client.publish("multi-projct.sound", splitData[1])


mess = ""
def readSerial():
    bytesToRead = ser.inWaiting()
    if (bytesToRead > 0):
        global mess
        mess = mess + ser.read(bytesToRead).decode("UTF-8")
        while ("#" in mess) and ("!" in mess):
            start = mess.find("!")
            end = mess.find("#")
            processData(mess[start:end + 1])
            if (end == len(mess)):
                mess = ""
            else:
                mess = mess[end+1:]

def Machine_ReleasePro(locate):
    ser.write((str(locate) + "#").encode())
    ser.write(("RELAY" + "#").encode())


def Machine_Check_Order_Queue():
    my_url = "https://thay-tam.herokuapp.com/api/v1/machine/order_queue"
    headers = {"Content-Type": "application/json",
               "X-MACHINE-UUID ": "uuid d89647bf-ebdb-53c5-ae26-99d5256439c5"}
    r = requests.get(url=my_url, headers=headers)

    print(r.json())
    order = r.json()
    print(order[0]["order_id"])



count30s=5
while True:
    if isMicrobitConnected:
        readSerial()

    if count30s <=0 :
        ser.write(("RESTART" + "#").encode())
    else:
        count30s -= 1
    # my_url = "https://thay-tam.herokuapp.com/api/v1/machine/order_queue"
    # headers = {"Content-Type": "application/json",
    #            "X-MACHINE-UUID ": "uuid d89647bf-ebdb-53c5-ae26-99d5256439c5"}
    # r = requests.get(url=my_url, headers=headers)


    # print(r)
    # print(r.json())
    # order = r.json()
    # print(order[0]["order_id"])


    # print(STO.Qty_find(STO,"Dasani"))
    # print(STO.Prod_add(STO,"Cream",5,1))
    time.sleep(1)