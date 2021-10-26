import gc
import network
import urequests as requests
import config
import time
from control import LedControl

from ntptime import settime

try:
    import usocket as socket
except:
    import socket

class WifiLevel():

    def __init__(self):
        gc.enable()

        self.apEssid=config.getValue('central-ap', 'essid')
        self.apPassword=config.getValue('central-ap', 'password')

        # NO Access Point
        ap_if = network.WLAN(network.AP_IF)
        ap_if.active(False)

        # Station
        self.wlan = network.WLAN(network.STA_IF)

        self.ledControl = LedControl()

        gc.collect()

    def connectToAp(self):

        self.ledControl.setBeforeConnection()
        gc.collect()

        counter = 0
        while not self.wlan.isconnected():

            phase = counter % 4

            print("connecting to network", "-\r" if phase == 0 else "\\\r" if phase == 1 else "|\r" if phase == 2 else "/\r",  end="")
            counter = counter + 1
            time.sleep(10)

            self.wlan.active(True)
            self.wlan.connect(self.apEssid, self.apPassword)
            gc.collect()

        print("                       \r", end="")
        print("ip: ", self.wlan.ifconfig()[0], end="")

        gc.collect()

    def getIfconfig(self):
        return self.wlan.ifconfig()

    def disconnectToAp(self):
        if self.wlan.isconnected():
            self.wlan.disconnect()

    def sendPost(self, address="192.168.4.1", path="", data="{}"):

        gc.collect()

        url = "http://" + address + "/" + path
        gc.collect()

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        gc.collect()

        self.connectToAp()
        gc.collect()

        try:

            # Indicate on the LED, sending POST
            self.ledControl.setBeforeSendPost()
            time.sleep(1)
            gc.collect()

            # Send the POST request

            print(" - POST ", end="")

                # Sync and convert time
#                settime()
#                utf=time.localtime()
#                timeStamp = "{}.{:02d}.{:02d}T{:02d}:{:02d}:{:02d}Z".format(utf[0], utf[1], utf[2], utf[3], utf[4], utf[5])
#                data['date'] = timeStamp

            gc.collect()

            r = requests.post(url, data=str(data), headers=headers)

            print(url, end="")
            print(":", r.status_code)

            gc.collect()

            # Indicate on the LED, sending was SUSSESSFUL
            self.ledControl.setPassedSendPost()

            gc.collect()

#               print(r.status_code, r.text)

        except Exception as e:

            # Indicate on the LED, sending FAILED
            self.ledControl.setFailedSendPost()

            print("!!! Network issue. Can not send request !!!", str(e))

            return False


        gc.collect()

        return True