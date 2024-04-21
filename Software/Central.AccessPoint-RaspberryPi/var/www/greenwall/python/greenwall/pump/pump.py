import requests
import logging
from datetime import datetime

class Pump:

    def __init__(self, web_gadget):

        self.webGadget = web_gadget

    def turnPumpOn(self, lengthInSec=0):

        for key, value in self.webGadget.registerPump.pumpDict.items():

            #dateString = datetime.fromtimestamp(value['timeStamp']).astimezone().isoformat()

            address = "http://{url}/pump/on?lengthInSec={lengthInSec}".format(url=value["ip"], lengthInSec=lengthInSec)
            data = {'lengthInSec': lengthInSec}

            try:
                x = requests.post(address, timeout=20)
                logging.debug("StatusCode: {0}".format(x.status_code))

            # NewConnectionError
            # ConnectTimeoutError
            except Exception as e:
                logging.error("Exception: {0}".format(e))

    def turnPumpOff(self):

        for key, value in self.webGadget.registerPump.pumpDict.items():

            #dateString = datetime.fromtimestamp(value['timeStamp']).astimezone().isoformat()

            address = "http://{url}/pump/off".format(url=value["ip"])

            try:
                x = requests.post(address, timeout=20)
                logging.debug("StatusCode: {0}".format(x.status_code))

            except Exception as e:
                logging.error("Exception: {0}".format(e))


    def getPumpStatus(self):

        addresses = []

        # TODO later I should handle more pumps. Now works only one
        for key, value in self.webGadget.registerPump.pumpDict.items():

            actDateTime = datetime.now().astimezone()
            actTimeStamp = datetime.timestamp(actDateTime)
            regTimeStamp = value["timeStamp"]
            diffSec = (actTimeStamp - regTimeStamp)

            # if less than 120 seconds was re-registering
            if diffSec < 120:
                addresses.append("http://{url}/pump/status".format(url=value["ip"]))

        try:
            address = addresses[0]

            x = requests.get(address, timeout=20)
            response = x.json()

            logging.debug("StatusCode: {0}".format(x.status_code))

            if x.status_code == 200:
                logging.debug("Response: {0}".format(x.text))
                return response.get('status')
            else:
                logging.error("Response: Failed. Status is n/a")
                return 'n/a'

        # NewConnectionError
        # ConnectTimeoutError
        except Exception as e:

            if len(addresses) == 0:
                logging.error("No pump registered.")
            else:
                logging.error("Exception: {0}. Status is n/a".format(e))
            return 'n/a'
