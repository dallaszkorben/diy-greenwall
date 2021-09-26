import gc
import network
import urequests as requests
import config
import time
from control import LedControl
try:
    import usocket as socket
except:
    import socket

class WifiLevel():

    def __init__(self):
        gc.enable()

        self.apEssid=config.getValue('central-ap', 'essid')
        self.apPassword=config.getValue('central-ap', 'password')

        ap_if = network.WLAN(network.AP_IF)
        ap_if.active(False)

        self.wlan = network.WLAN(network.STA_IF)

        self.ledControl = LedControl()

        gc.collect()

    def connectToAp(self):

        gc.collect()

        if self.wlan.isconnected():
            print("disconnecting from network...")
            self.wlan.disconnect()

        self.wlan.active(True)

        gc.collect()

#        if not self.wlan.isconnected():
        print("connecting to network...")
#        wlan.ifconfig(('192.168.4.20', '255.255.255.0', '192.168.4.1', '192.168.4.1'))
        self.wlan.connect(self.apEssid, self.apPassword)

        self.ledControl.noAp()

        while not self.wlan.isconnected():
            print("Waiting for isconnected()")
            time.sleep(10)
        self.ledControl.isAp()
        print("connected")
        print("network config:", self.wlan.ifconfig())

        gc.collect()

#        return self.wlan

    def getIfconfig(self):
        return self.wlan.ifconfig()

    def disconnectToAp(self):
        if self.wlan.isconnected():
            self.wlan.disconnect()

    def sendPost(self, address="192.168.4.1", path="", data="{}"):

        gc.collect()

        url = "http://" + address + "/" + path
        print(url)

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }


#        gc.collect()

#        if not self.wlan.isconnected():
#            self.connectToAp()

        gc.collect()

        try:
            self.ledControl.isAp()

            r = requests.post(url, data=str(data), headers=headers)

            self.ledControl.isWeb()

            print(r.status_code, r.text)

        except Exception as e:
            self.ledControl.noWeb()

            print("!!! Network issue !!!", str(e))

            self.connectToAp()
#    r = requests.get(url, headers=headers)

        gc.collect()

#    results = r.json()
#    print(results)


