from micropyserver import MicroPyServer
import json
import network
import gc
import ubinascii
import time
from ntptime import settime

class WifiCentral():

    HIDDEN=False

    def __init__(self):

        gc.enable()

        self.server = None

        print()
        print("***************************")
        print("Connect to Home Wifi...")
        homeWifiEssid = "blabla2.4"
        homeWifiPassword = "Elmebetegek Almaiban"
        self.sta = network.WLAN(network.STA_IF)
        if not self.sta.isconnected():
            self.sta.active(True)
            gc.collect()

            self.sta.connect(homeWifiEssid, homeWifiPassword)
            gc.collect()
        while not self.sta.isconnected():
            print(" Waiting for isconnected()")
            time.sleep(10)

        print(" Connected")
        print(" Network config:", self.sta.ifconfig())
        print("***************************")
        print()

        print("***************************")
        print("Configuring Access Point...")
        self.ap = network.WLAN(network.AP_IF)
        self.ap.active(True)
        self.ap.config(essid='Central-Station-006', password="viragfal", hidden=WifiCentral.HIDDEN)

        while self.ap.active() == False:
          pass

        print(' Access Point is done')
        print(" essid: ", self.ap.config("essid"))
        print(" ifconfig: ", self.ap.ifconfig())
        print(" mac: ", ubinascii.hexlify(self.ap.config("mac"), ":").decode())
        print("***************************")
        print()

        settime()

        self.count = 0

        gc.collect()

    def return_json(self, request, data):
        ''' request handler '''
        request

        utf=time.localtime()
        timeStamp = "{}.{:02d}.{:02d}T{:02d}:{:02d}:{:02d}".format(utf[0], utf[1], utf[2], utf[3], utf[4], utf[5])

        self.count = self.count  + 1

        if data['variance'] <= 0.156:
#            print(data['variance'])
            print(self.count, timeStamp, data)
        else:
            print(".", end="")

        # return message
        json_str = json.dumps({"status": "ok"})
        self.server.send("HTTP/1.0 200 OK\r\n")
        self.server.send("Content-Type: application/json\r\n\r\n")
        self.server.send(json_str)

#        print("   ", gc.mem_free())
        gc.collect()

    def start(self):
        self.server = MicroPyServer()

        self.server.add_route(path="/levelreport", handler=self.return_json, method="POST")

        print("***************************")
        print("Waiting for request...")
        print("***************************")

        try:
            self.server.start()
        finally:
            self.server.close()

