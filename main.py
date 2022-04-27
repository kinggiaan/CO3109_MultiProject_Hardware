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

# global order_queue
# real

# order = []
# process_order = 0
# wait_release = 0

def get_serial_port():
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
if get_serial_port() != "None":
    global ser
    ser = serial.Serial( port=get_serial_port(), baudrate=115200)
    isMicrobitConnected = True

# {
#     "uuid": "baaa78dd-dbd4-4a2a-b0bd-7a071178d76c",
#     "order": {
#         "order_item_set": [
#             {
#                 "item": {
#                     "uuid": "6d9349b0-7877-5f44-a863-888e273c3ab0",
#                     "name": "Coca Cola"
#                 },
#                 "quantity": 1
#             },
#             {
#                 "item": {
#                     "uuid": "ce602c59-de2e-5dfb-8841-02e1d719b1d4",
#                     "name": "Coca Light"
#                 },
#                 "quantity": 1
#             }
#         ]
#     }
# }

mess = ""
def process_data(data):
  
    
    data = data.replace("!", "")
    data = data.replace("#", "")
    splitData = data.split(":")
    
    #print(splitData)
    #splitData[0] = input(str)
    if splitData[0] == "TIME_OUT":
         #Or hien tai da Time Out va quay ve hang doi
         ser.write("TIME_OUT_LCD" + "#").encode()
         print("TIME_OUT_LCD")
         print("NEXT_PRODUCT")
    
    # if splitData[0] == "DONE_ORDER" :
    #     #ser.write("DONE_ORDER"  "#").encode())
    #     complete_order(order["uuid"])
    # if splitData[0] == "BUTTON":
    #     ser.write("BUTTON"+"#").encode()
    #     print("BUTTON")

mess = ""
def read_serial():
    bytesToRead = ser.inWaiting()
    if (bytesToRead > 0):
        global mess
        mess = mess + ser.read(bytesToRead).decode("UTF-8")
        while ("#" in mess) and ("!" in mess):
            start = mess.find("!")
            end = mess.find("#")
            process_data(mess[start:end + 1])
            if (end == len(mess)):
                mess = ""
            else:
                mess = mess[end+1:]


#MACHINE FUNCTION
def Machine_Wait_taken():
    ser.write(("TAKEN_YET" + "#").encode())
    print("WAIT_TAKEN")

def Machine_Out_of_Product():
    ser.write(("OUT_OF_PROD" + "#").encode())
    print("OUT_OF_PRODUCT")

def Machine_Start_Oder():
    ser.write(("START" + "#").encode())
    print("START ORDER")

def Machine_Done_Order():
    ser.write(("DONE_ORDER" + "#").encode())
    print("DONE_ORDER")

def Machine_ReleasePro(name,locate , qty):
    ser.write((str(locate) + "#").encode())
    time.sleep(2)
    ser.write(("RELAY" + "#").encode())
    STO.Qty_realese(STO, name, qty)
    print("Release " + str(name) + " " +str(qty))
    #test
    print(STO.Qty_find(STO, name))

def Machine_No_Order():
    ser.write(("NO_ORDER" + "#").encode())
    print("NO_ORDER")

def Machine_Scan_Quantity(product):
    if product["quantity"] > STO.Qty_find(STO, product["name"]):
        return False
    return True

def get_next_order():
    url = "https://thay-tam.herokuapp.com/api/v1/machine/next"
    headers = {"Content-Type": "application/json",
               "X-MACHINE-UUID ": "uuid d89647bf-ebdb-53c5-ae26-99d5256439c5"}
    response = requests.get(url=url, headers=headers)
    return response.status_code, response.json()

def get_item_queue(order_data):
    item_set = order_data["order"]["order_item_set"]
    return [{"name": i["item"]["name"], "quantity": i["quantity"]} for i in item_set]

def invalidate_order(order_uuid):
    url = "https://thay-tam.herokuapp.com/api/v1/machine/invalidate"
    headers = {"Content-Type": "application/json"}
    data = {"order_uuid": order_uuid}
    response = requests.post(url=url, data=data, headers=headers)
    return response.status_code

def complete_order(order_uuid):
    url = "https://thay-tam.herokuapp.com/api/v1/machine/complete"
    headers = {"Content-Type": "application/json"}
    data = {"order_uuid": order_uuid[1:-1]}
    response = requests.post(url=url, data=data, headers=headers)
    print(response.json())
    return response.status_code

while True:
    #Microbit ser.read
    if isMicrobitConnected:
        read_serial()
        status_code, order = get_next_order()
        if status_code == 200:
            item_queue = get_item_queue(order)

            # Scan product
            is_available = True
            for product in item_queue:
                if not Machine_Scan_Quantity(product):
                    is_available = False
                    Machine_Out_of_Product()

                    # REQUEST BAO KHONG DU HANG
                    invalidate_order(order["uuid"])
                    order.clear()
                    break

            # de nha Order hien tai ra va relay nhay on off on
            # release
            if is_available:
                for product in item_queue:
                    Machine_ReleasePro(product["name"], STO.Locate_find(STO,product["name"]),product["quantity"])
                    time.sleep(3)
                Machine_Wait_taken()
                # Wait 10s for User take order
                time.sleep(7)
                Machine_Done_Order()
                complete_order(order["uuid"])
        else:
            Machine_No_Order()
            time.sleep(5)
    else:
        time.sleep(1)
