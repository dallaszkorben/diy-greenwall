import gc
import network
import machine
import urequests as requests
import config
import time
import utime
from representations import output_json
import json

from common import getOffsetDateString
from common import LedControl

try:
    import usocket as socket
except:
    import socket

class WifiControl():

    def __init__(self):
        gc.enable()

        print('==========================')
        print('=== Initialize Network ===')
        print('==========================')

        self.apEssid=config.getValue('central-ap', 'essid')
        self.apPassword=config.getValue('central-ap', 'password')
        self.apIp=config.getValue('central-ap', 'webserver-ip')
        self.apWebServerPathInfoTimestamp=config.getValue('central-ap', 'webserver-path-info-timestamp')

        # NO Access Point
        ap_if = network.WLAN(network.AP_IF)
        ap_if.active(False)

        # Station
        self.wlan = network.WLAN(network.STA_IF)

        self.ledControl = LedControl()

        self.syncTime()

        print('==========================')

        gc.collect()

    def connectToAp(self):

        if not self.wlan.isconnected() or self.wlan.ifconfig()[0] == "0.0.0.0":
            self.wlan.active(True)
            self.wlan.connect(self.apEssid, self.apPassword)

            counter = 0
            while not self.wlan.isconnected():
                time.sleep(1)

                phase = counter % 4
                print("Connecting to network {0} {1}s{2}".format("-" if phase == 0 else "\\" if phase == 1 else "|" if phase == 2 else "/", counter, "\r"),  end="")
                counter += 1

        if self.wlan.isconnected():

            print("Connected to {0}. My IP: {1}".format(self.apIp, self.wlan.ifconfig()[0]))
            return output_json(success=True)

        else:

            print("!!! Connection failed !!!")
            return output_json(success=False)

    def disconnectToAp(self):
        if self.wlan.isconnected():
            self.wlan.disconnect()

    def getIfconfig(self):
        return self.wlan.ifconfig()

    def sendRest(self, type="POST", address="192.168.4.1", path="", data="{}"):
        """
            return: Object
                            .status_code
                            .text
                                {
                                    "result: 'OK',
                                    ...
                                }
        """
        #gc.collect()

        # Indicate on the LED, BEFORE CONNECTION
        self.ledControl.setBeforeConnection()


        url = "http://" + address + "/" + path
        #gc.collect()

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        #gc.collect()

        conn = self.connectToAp()
        #gc.collect()

        if conn['success']:

            # Indicate on the LED, BEFORE SENDING REST
            self.ledControl.setBeforeSendRest()

            # Send the POST request
            print(" - POST " if type == "POST" else " - GET ", end="")
            print(url, data, end=" ")

            MAX_LOOP = 20
            cycle = 0
            while cycle < MAX_LOOP:
                exception = ""

                time.sleep(4)

                try:

                    if type == "POST":
                        r = requests.post(url, data=str(data), headers=headers)
                    else:
                        r = requests.get(url, data=str(data), headers=headers)

                    print(" - Response: {0}, {1}".format(r.status_code, r.text))

                    # Indicate on the LED, sending was SUSSESSFUL
                    self.ledControl.setPassedSendRest()

                    conn = output_json(success=True, data=json.loads(r.text))
                    break

                except Exception as e:

                    exception = e
                    print(".", end="")

                cycle+=1

            if cycle >= MAX_LOOP:

                # Indicate on the LED, sending FAILED
                self.ledControl.setFailedSendRest()

                print("!!! Network issue. Can not send request !!!", str(exception))

                conn = output_json(success=False)

        else:

            # Indicate on the LED, FAILED CONNECTION
            self.ledControl.setFailedConnection()

        return conn

    def syncTime(self):

        result = {'success': False}

        while not result['success']:
            #timeutime.localtime(0)
            epocDate = "2000.01.01"
            #data = ujson.dumps({'epocDate': epocDate})
            result = self.sendRest(type="GET", address=self.apIp, path=self.apWebServerPathInfoTimestamp + "/epocDate/" + epocDate)
            time.sleep(1)

        timeStamp = result['data']['timeStamp']
        date = utime.localtime(timeStamp)
        correctedDate = (date[0], date[1], date[2], 0, date[3], date[4], date[5], 0)
        machine.RTC().datetime(correctedDate)
        print("Synchronized time: {0}".format(getOffsetDateString(utime.localtime())))


