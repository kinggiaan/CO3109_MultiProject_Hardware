# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import random
# import pyowm  

import serial.tools.list_ports
import time
import sys
import requests
import json
import Storage as STO


# #test
# product_info = []
# order = [{'machine_uuid': 'd89647bf-ebdb-53c5-ae26-99d5256439c5', 'order_uuid': '4ad6ece6-8e17-59ac-b140-a7afb9b77fbd', 'item': {'uuid': 'e5fb8ff4-9520-5118-8195-290803e57460', 'image': '/media/products/dasani.png', 'name': 'Dasani', 'price': 25}, 'quantity': 1}, {'machine_uuid': 'd89647bf-ebdb-53c5-ae26-99d5256439c5', 'order_uuid': '4ad6ece6-8e17-59ac-b140-a7afb9b77fbd', 'item': {'uuid': '072c8269-eda2-5085-8d5f-4811e5adb80d', 'image': '/media/products/sting.png', 'name': 'Sting', 'price': 35}, 'quantity': 2}, {'machine_uuid': 'd89647bf-ebdb-53c5-ae26-99d5256439c5', 'order_uuid': 'de6f909e-78c7-5be4-8e88-29aa60c4320a', 'item': {'uuid': 'ba50b773-0580-5da1-b4fa-56f01696a1cb', 'image': '/media/products/blackcoffee.png', 'name': 'Black Coffee', 'price': 70}, 'quantity': 1}, {'machine_uuid': 'd89647bf-ebdb-53c5-ae26-99d5256439c5', 'order_uuid': 'de6f909e-78c7-5be4-8e88-29aa60c4320a', 'item': {'uuid': 'baf9c355-a040-5f07-a669-a92e6245bf3e', 'image': '/media/products/nutriboost.png', 'name': 'NutriBoost', 'price': 30}, 'quantity': 1}]
# process_order = 0
# wait_release = 0

global order_queue
#real
product_info = []
order = []
process_order = 0
wait_release = 0

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
    global ser
    ser = serial.Serial( port=getPort(), baudrate=115200)
    isMicrobitConnected = True


mess = ""
def processData(data):
    global process_order
    global product_info
    global wait_release
    data = data.replace("!", "")
    data = data.replace("#", "")
    splitData = data.split(":")
    print(splitData)
    splitData[0] = input(str)
    if splitData[0] == "BUTTON" and process_order == 1 and wait_release ==1 : #de nha sp ra va relay nhay on off on
        Machine_ReleasePro(product_info["name"], product_info["locate"], order[0]["quantity"])
        Request_Delete_Order()


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
#ORDER QUEUE REQUEST
def Request_Oder_Queue():
    global order
    my_url = "https://thay-tam.herokuapp.com/api/v1/machine/order_queue"
    headers = {"Content-Type": "application/json",
               "X-MACHINE-UUID ": "uuid d89647bf-ebdb-53c5-ae26-99d5256439c5"}
    r = requests.get(url=my_url, headers=headers)
    print(r.json())
    order = r.json()
    print("")

def Request_Delete_Order(order_uuid):

    global order
    my_url = "https://thay-tam.herokuapp.com/api/v1/machine/clear_order"
    # headers = {"Content-Type": "application/json",
    #             "X-MACHINE-UUID": "uuid d89647bf-ebdb-53c5-ae26-99d5256439c5"
    #            }
    data = {
        "order_uuid" : f"{order_uuid}"
    }
    r = requests.post(url=my_url, data=data)
    print(r.json())
    order = r.json()
    print("")
    process_order = 0
    del order[0]
    print(order)
    print("Next order!!!")

#MACHINE FUNCTION
def Machine_Out_of_Product():
    # ser.write(("OUT_OF_PROD" + "#").encode())
    print("OUT_OF_PRODUCT")

def Machine_Update_Temp_Moi():
    print("Update temp request")
    #ser.write(("RESTART_TEMP" + "#").encode())

def Machine_ReleasePro(name, locate, qty):
    #ser.write((str(locate) + "#").encode())
    #ser.write(("RELAY" + "#").encode())
    STO.Qty_realese(STO, name, qty)
    print("Release " + str(name) + " " +str(qty))
    #test
    print(STO.Qty_find(STO, name))

def Machine_No_Order():
    #ser.write(("NO_ORDER" + "#").encode())
    print("NO_ORDER")

def Check_Order_Queue():
    global order
    global product_info
    global process_order
    global wait_release
    # check how many order
    if print(len(order)) == 0:
        Machine_No_Order()
    else:
        process_order = 1
        # check the first oder
        #print(order[0]["order_id"])
        print(order[0]["item"]["name"])
        if STO.Qty_find(STO, order[0]["item"]["name"]) >= order[0]["quantity"]:
            product_info = STO.Product_find(STO, order[0]["item"]["name"])

            # Send to Microbit to chang Relay by Location of Product
            #Machine_ReleasePro(product_info["name"], product_info["locate"], order[0]["quantity"])

            #Wait for button to Release Product
            wait_release = 1
            #Send request back sever to delete Order

        else:
            Machine_Out_of_Product()

        #Delete order in queue if not wait for release product
        if wait_release == 0:
            Request_Delete_Order(order[0]["order_uuid"])


# TODO Quy trình order trực tiếp trên PC
# Thêm 1 file .py -> Hiện thị các sản phẩm đang có trong kho, nhận lệnh (class)
# Hiện thi Menu lệnh  
# TODO 1. Nhấn enter để khởi tạo 
# TODO 2. Nhấn button để chọn order => thêm vào 1 queue
# TODO 3. Nhấn enter để chốt order & nhả nước => chuyển order queue sang queue để nhả nước
# TODO 3.5 Nhấn clear để xóa order
# TODO 4. Lưu vào 1 data storage chung, lí tưởng là database, không thì dùng 1 queue ở mức độ global
# TODO 5. 1 hàm chuyên đọc data storage rồi xử lý queue
# TODO 6. Giả sử cấu trúc element trong queue là { 'online': '', **data }
# TODO nếu đọc được online = True => sau khi nhả nước -> gọi clear_order


count30s = 0
count_request = 0
while True:
    #if isMicrobitConnected:
    #test gateway
    # TODO Hứng trigger từ button
    if True:
        #readSerial()
        if order and not wait_release:
            Check_Order_Queue()
        elif order and wait_release:
            processData("!TEST#")
        elif not order:
            Machine_No_Order()
        if count30s <= 0:
            # send request to ask  order queue
            Request_Oder_Queue()
            count30s = 5
        else:
            count30s -= 1

    time.sleep(1)