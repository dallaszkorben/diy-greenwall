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

        self.ledControl.setBeforeConnection()

        gc.collect()

#        if not self.wlan.isconnected():

        self.wlan.active(True)

        gc.collect()

        print("connecting to network...")

        self.wlan.connect(self.apEssid, self.apPassword)

        gc.collect()

#        while not self.wlan.isconnected():
#            print("Waiting for isconnected()")
#            time.sleep(10)
#
#        print("connected")
#        print("network config:", self.wlan.ifconfig())
#
#        gc.collect()


    def isConnectedToAp(self):
        self.connectToAp()

        counter = 1
        threshold = 10
        while not self.wlan.isconnected() and threshold > counter:

            print("Waiting for isconnected() (", counter, ")")

            counter = counter + 1

            time.sleep(5)

        # connection was successful
        if counter <= threshold:

            print("connected")
            print("network config:", self.wlan.ifconfig())
            return True

        else:

            # Indicate on the LED, NO CONNECTION to Access Point
            self.ledControl.setFailedConnection()
            print("!!! No Connection issue !!!")

            return False


#    def isConnected(self):
#        return self.wlan.isconnected()

    def getIfconfig(self):
        return self.wlan.ifconfig()

#    def disconnectToAp(self):
#        if self.wlan.isconnected():
#            self.wlan.disconnect()

    def sendPost(self, address="192.168.4.1", path="", data="{}"):


        if self.isConnectedToAp():

            url = "http://" + address + "/" + path
            print("Send POST to: ", url)

            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }

            gc.collect()

            try:

                # Indicate on the LED, sending POST
                self.ledControl.setBeforeSendPost()
                time.sleep(1)

                # Send the POST request
                r = requests.post(url, data=str(data), headers=headers)

                # Indicate on the LED, sending was SUSSESSFUL
                self.ledControl.setPassedSendPost()

                print(r.status_code, r.text)

            except Exception as e:

                # Indicate on the LED, sending FAILED
                self.ledControl.setFailedSendPost()

                print("!!! Network issue !!!", str(e))


            gc.collect()
