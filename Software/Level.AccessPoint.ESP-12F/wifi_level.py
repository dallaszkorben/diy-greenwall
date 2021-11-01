from micropyserver import MicroPyServer
import json
import network
import gc
import ubinascii
#import time
import config
#import os
#from machine import Timer
#from ntptime import settime
#from linreg import LinReg
from water_level_sensor import WaterLevelSensor

class WifiLevel():

    HIDDEN=False

    def __init__(self):

        gc.enable()

        self.server = None

        # read configuration
        self.levelApEssid=config.getValue('level-ap', 'essid')
        self.levelApPassword=config.getValue('level-ap', 'password')

        pinAnalog=config.getValue('water-level-sensor', 'analog-pin')
        m=config.getValue('water-level-sensor', 'linear-m')
        b=config.getValue('water-level-sensor', 'linear-b')
        sampleNumber=config.getValue('water-level-sensor', 'sample-number')
        maximumVariance=config.getValue('water-level-sensor', 'maximum-variance')

        print("***************************")
        print("Configuring Access Point...")
        self.ap = network.WLAN(network.AP_IF)
        self.ap.active(True)

        self.ap.config(essid=self.levelApEssid, password=self.levelApPassword, hidden=WifiLevel.HIDDEN)

        while self.ap.active() == False:
          pass

        #self.ap.ifconfig(('192.168.5.1', '255.255.255.0', '192.168.5.1', '192.168.5.1'))

        print(' Access Point is done')
        print(" essid: ", self.ap.config("essid"))
        print(" ifconfig: ", self.ap.ifconfig())
        print(" mac: ", ubinascii.hexlify(self.ap.config("mac"), ":").decode())
        print("***************************")
        print()

        self.wls=WaterLevelSensor(pinAnalog, sampleNumber, m, b)

        self.count = 0

        gc.collect()

    def get_info(self, request, data):

        print(request)
        gc.collect()

        level = self.wls.getLevelMeanInMm()
        gc.collect()

        json_response = {}
        json_response['level'] = level[0]
        json_response['measurement'] = "mm"
        json_response['variance'] = level[1]

        string_response = json.dumps(json_response)
        self.server.send("HTTP/1.0 200 OK\r\n")
        self.server.send("Content-Type: text/plain\r\n\r\n")
        self.server.send(string_response)

        self.count = self.count  + 1

        gc.collect()

    def start(self):
        self.server = MicroPyServer()

        self.server.add_route(path="/info", handler=self.get_info, method="GET")

        print("***************************")
        print("Waiting for request...")
        print("***************************")

        self.server.start()
