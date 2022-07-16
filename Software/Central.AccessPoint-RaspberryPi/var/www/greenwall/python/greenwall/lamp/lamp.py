import requests
import logging
from datetime import datetime

class Lamp:

    def __init__(self, web_gadget):

        self.webGadget = web_gadget

    def turnLampOn(self, lengthInSec=0):

        for key, value in self.webGadget.registerLamp.lampDict.items():

            address = "http://{url}/lamp/on?lengthInSec={lengthInSec}".format(url=value["ip"], lengthInSec=lengthInSec)
            data = {'lengthInSec': lengthInSec}

            try:
                x = requests.post(address, timeout=20)
                logging.debug("StatusCode: {0}".format(x.status_code))

            # NewConnectionError
            # ConnectTimeoutError
            except Exception as e:
                logging.error("Exception: {0}".format(e))

    def turnLampOff(self, lengthInSec=0):

        for key, value in self.webGadget.registerLamp.lampDict.items():

            address = "http://{url}/lamp/off?lengthInSec={lengthInSec}".format(url=value["ip"], lengthInSec=lengthInSec)
            data = {'lengthInSec': lengthInSec}

            try:
                x = requests.post(address, timeout=20)
                logging.debug("StatusCode: {0}".format(x.status_code))

            except Exception as e:
                logging.error("Exception: {0}".format(e))

    def getLampStatus(self):

        addresses = []

        # TODO later I should handle more lamps. Now works only one
        for key, value in self.webGadget.registerLamp.lampDict.items():

            actDateTime = datetime.now().astimezone()
            actTimeStamp = datetime.timestamp(actDateTime)
            regTimeStamp = value["timeStamp"]
            diffSec = (actTimeStamp - regTimeStamp)

            # if less than 120 seconds was re-registering
            if diffSec < 120:
                addresses.append("http://{url}/lamp/status".format(url=value["ip"]))

        try:

            address = addresses[0]

            x = requests.get(address, timeout=20)
            response = x.json()

            logging.debug("Lamp StatusCode: {0}".format(x.status_code))

            if x.status_code == 200:
                logging.debug("Lamp Status Response: {0}".format(x.text))
                return response.get('status')
            else:
                logging.error("Lamp Status Response: Failed. Status is n/a")
                return 'n/a'


        # NewConnectionError
        # ConnectTimeoutError
        except Exception as e:

            if len(addresses) == 0:
                logging.debug("No lamp registered.")
            else:
                logging.error("Exception: {0}. Status is n/a".format(e))
            return 'n/a'
