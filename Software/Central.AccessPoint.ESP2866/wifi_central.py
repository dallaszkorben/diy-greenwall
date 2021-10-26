from micropyserver import MicroPyServer
import json
import network
import gc
import ubinascii
import time
import config
import os
from machine import Timer
from ntptime import settime
from linreg import LinReg

class WifiCentral():

    HIDDEN=True

    def __init__(self):

        gc.enable()

        self.server = None

        self.centralApEssid=config.getValue('central-ap', 'essid')
        self.centralApPassword=config.getValue('central-ap', 'password')
        self.homeApEssid=config.getValue('home-ap', 'essid')
        self.homeApPassword=config.getValue('home-ap', 'password')

        print()
        print("***************************")
        print("Connect to Home Wifi...")
        self.sta = network.WLAN(network.STA_IF)
        if not self.sta.isconnected():
            self.sta.active(True)
            gc.collect()

            self.sta.connect(self.homeApEssid, self.homeApPassword)
            gc.collect()
        counter = 0
        while not self.sta.isconnected():
            if counter >= 3:
                break
            else:
                print(" Waiting for isconnected()")
            time.sleep(10)
            counter = counter + 1

        if counter >= 3:
            print(" NOT connected")
        else:
            print(" Connected")
            print(" Network config:", self.sta.ifconfig())

        print("***************************")
        print()

        print("***************************")
        print("Configuring Access Point...")
        self.ap = network.WLAN(network.AP_IF)
        self.ap.active(True)
        self.ap.config(essid=self.centralApEssid, password=self.centralApPassword, hidden=WifiCentral.HIDDEN)

        while self.ap.active() == False:
          pass

        print(' Access Point is done')
        print(" essid: ", self.ap.config("essid"))
        print(" ifconfig: ", self.ap.ifconfig())
        print(" mac: ", ubinascii.hexlify(self.ap.config("mac"), ":").decode())
        print("***************************")
        print()

        # Sync time periodiaclly by 1 h
#        tim = Timer(10)
#        tim.init(period=3600000, mode=Timer.PERIODIC, callback=self.syncTime)
#        self.syncTime()

        self.count = 0

        gc.collect()

    def syncTime(self, tim=""):
        print(time, "sync\r", end="")

        counter = 0
        while not self.sta.isconnected():

            # No sync if it is not possible to connect more than 20 seconds
            if counter > 20:
                print("sync NO                    ")
                return

            phase = counter % 4

            print("sync. connecting to wifi", "-\r" if phase == 0 else "\\\r" if phase == 1 else "|\r" if phase == 2 else "/\r",  end="")
            counter = counter + 1
            time.sleep(1)

            self.sta.active(True)
            self.sta.connect(self.homeApEssid, self.homeApPassword)
            gc.collect()

        try:
            settime()
            print("sync Done                  ")
        except Exception as e:
            print("sync Error: {0}            ".format(e))

        gc.collect()

    def post_level_report(self, request, data):
        ''' request handler '''
        request

        if self.count % 100 == 0:
            self.syncTime()

        utf=time.localtime()
        dateTime = "{}.{:02d}.{:02d}T{:02d}:{:02d}:{:02d}Z".format(utf[0], utf[1], utf[2], utf[3], utf[4], utf[5])

        with open('report.log', 'a') as f:
            f.write(str(time.time()))
            f.write(" ")
            f.write(data['id'])
            f.write(" ")
            if 'value' in data:
                f.write(str(data['value']))
                f.write(" ")
            if 'variance' in data:
                f.write(str(data['variance']))
                f.write(" ")
            f.write("\n")

        gc.collect()

#        if 'variance' in data and data['variance'] <= 0.5:
        stat = os.statvfs('/')
        print(self.count, dateTime, data, stat[0]*stat[3])
#        else:
#            print(".", end="")

        # return message
        json_str = json.dumps({"status": "ok"})
        self.server.send("HTTP/1.0 200 OK\r\n")
        self.server.send("Content-Type: application/json\r\n\r\n")
        self.server.send(json_str)

        self.count = self.count  + 1

        gc.collect()

    def get_info(self, request, data):

        gc.collect()

        #list_response = []
        x = []
        y = []
        string_response = ""
        with open('report.log', 'r') as f:
            while True:
                line = f.readline()
                if not line:
                    break

                collection = line.split(" ")

                x.append(int(collection[0]))
                y.append(int(collection[2]))

        gc.collect()

        lr = LinReg(x,y)
        coef = lr.getCoef()
        string_response = "m: " + str(coef[0]) + " b: " + str(coef[1]) + "\n"
        string_response += "change: " + str(coef[0]*86400) + " mm/day\n"
        string_response += "change: " + str(coef[0]*604800) + " mm/week\n"

        #json_response = json.dumps(list_response)
        self.server.send("HTTP/1.0 200 OK\r\n")
        self.server.send("Content-Type: text/plain\r\n\r\n")
        self.server.send(string_response)

        self.count = self.count  + 1

        gc.collect()

    def start(self):
        self.server = MicroPyServer()

        self.server.add_route(path="/levelreport", handler=self.post_level_report, method="POST")

        self.server.add_route(path="/info", handler=self.get_info, method="GET")

        print("***************************")
        print("Waiting for request...")
        print("***************************")

        self.server.start()
