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
        #ap_if = network.WLAN(network.AP_IF)
        #ap_if.active(False)

        # Station
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        self.wlan.connect(self.apEssid, self.apPassword)

        self.ledControl = LedControl()
        #gc.collect()

    def connectToAp(self):

        self.ledControl.setBeforeConnection()

        self.wlan.active(True)
        self.wlan.connect(self.apEssid, self.apPassword)

        counter = 0
        while (not self.wlan.isconnected() or self.wlan.ifconfig()[0] == "0.0.0.0" ) and counter < 50:
            time.sleep(1)

            phase = counter % 4
            print("connecting to network", "-\r" if phase == 0 else "\\\r" if phase == 1 else "|\r" if phase == 2 else "/\r",  end="")
            counter = counter + 1

        print("                       \r", end="")

        if not self.wlan.isconnected():
            print("!!! Connection interrupted !!!")
            return False

        else:
            print("ip: ", self.wlan.ifconfig()[0], end="")
#            print("ip: ", "\U0001f44d" if counter == 0 else " ",self.wlan.ifconfig()[0], end="")
            return True

    def getIfconfig(self):
        return self.wlan.ifconfig()

    def disconnectToAp(self):
        if self.wlan.isconnected():
            self.wlan.disconnect()

    def sendPost(self, address="192.168.4.1", path="", data="{}"):

        #gc.collect()

        url = "http://" + address + "/" + path
        #gc.collect()

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        #gc.collect()

        conn = self.connectToAp()
        #gc.collect()

        if conn:

            # Indicate on the LED, sending POST
            self.ledControl.setBeforeSendPost()
#            time.sleep(1)
#            gc.collect()

            # Send the POST request
            print(" - POST ", end="")

            cycle = 0
            while cycle < 10:
                exception = ""

                time.sleep(4)

                try:

                    r = requests.post(url, data=str(data), headers=headers)

                    print(url, end="")
                    print(" - response status:", r.status_code, "      ", gc.mem_free())

                    # Indicate on the LED, sending was SUSSESSFUL
                    self.ledControl.setPassedSendPost()

                    break

                except Exception as e:

                    exception = e
                    print(".", end="")

                cycle+=1

            if cycle >= 10:
                self.ledControl.setFailedSendPost()
                print("!!! Network issue. Can not send request !!!", str(exception))
                conn = False

        return conn
