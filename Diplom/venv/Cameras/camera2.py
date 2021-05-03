import pyautogui
from PIL import Image
import websockets as ws
import asyncio
import base64
from io import BytesIO
from threading import Thread
import os
import requests
import cv2

class DataProvider(Thread):
    def __init__(self):
        Thread.__init__(self)


    def run(self):
        global data
        cam = cv2.VideoCapture(0)
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
        while True:
            ret, frame = cam.read()
            result, sframe = cv2.imencode('.jpg', frame, encode_param)
            data = base64.b64encode(sframe)
async def send_images(websocket, path):
    print(f"Client connected")
    global data
    try:
        while True:
            await websocket.send(data)
            await asyncio.sleep(0.05)
    except:
        print("Client closed")


def check_rules():
    try:
        response = requests.post(f"{params['http_server']}/check_camera",
                                 data={'id': params['id'], 'address': params['address'], 'port': params['port']}).json()
        if response["type"] == "success":
            return True
        elif response["type"] == "error":
            print(response["message"])
            return False
    except:
        print("Http request error")
        return False


def start_data_provider():
    try:
        data_provider = DataProvider()
        data_provider.start()
        return True
    except:
        print("Data recording error")
        return False


def start_broadcast():
    try:
        try:
            response = requests.post(f"{params['http_server']}/run_camera", data={'id': params['id'], 'address': params['address'], 'port': params['port']}).json()
            if response["type"] == "success":
                print("Camera started")
				#print("Camera started : id  ; ip  ; port  ")
        except:
            print("Http request error")
        send_images_serve = ws.serve(send_images, params['address'], params['port'])
        asyncio.get_event_loop().run_until_complete(send_images_serve)
        asyncio.get_event_loop().run_forever()
    except:
        try:
            requests.post(f"{params['http_server']}/stop_camera", data={'id': params['id'], 'address': params['address'], 'port': params['port']})
            print("Broadcast creating error")
        except:
            print("Http request error")


global data

config = open("Cameras/cameraConfig.cfg", "r").readlines()
params = dict()

for line in config:
    p_name, p_val = line.split("=")
    params[p_name.strip()] = p_val.strip()


	
if check_rules():
    if start_data_provider():
        start_broadcast()
		
print("Configs : id\t= ("+params['id']+") \nConfigs : ip\t= ("+params['address']+") \nConfigs : post\t= ("+params['port']+")")
		
input("Press Enter to exit...")
os._exit(1)
