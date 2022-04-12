import requests
import logging

class Lamp:

    def __init__(self, web_gadget):

        self.webGadget = web_gadget

    def turnLampOn(self, lengthInSec=0):

        for key, value in self.webGadget.registerLamp.lampDict.items():

            #dateString = datetime.fromtimestamp(value['timeStamp']).astimezone().isoformat()

            address = "http://{url}/lamp/on?lengthInSec={lengthInSec}".format(url=value["ip"], lengthInSec=lengthInSec)
            data = {'lengthInSec': lengthInSec}

#            logging.debug("Request: {0}".format(address))

            try:
                x = requests.post(address, timeout=20)
                logging.debug("StatusCode: {0}".format(x.status_code))

            # NewConnectionError
            # ConnectTimeoutError
            except Exception as e:
                logging.error("Exception: {0}".format(e))

    def turnLampOff(self, lengthInSec=0):

        for key, value in self.webGadget.registerLamp.lampDict.items():

            #dateString = datetime.fromtimestamp(value['timeStamp']).astimezone().isoformat()

            address = "http://{url}/lamp/off?lengthInSec={lengthInSec}".format(url=value["ip"], lengthInSec=lengthInSec)
            data = {'lengthInSec': lengthInSec}

#            logging.debug("Request: {0}".format(address))

            try:
                x = requests.post(address, timeout=20)
                logging.debug("StatusCode: {0}".format(x.status_code))

            except Exception as e:
                logging.error("Exception: {0}".format(e))



