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



    def getLampStatus(self):

        addresses = []

        # TODO later I should handle more lamps. Now works only one
        for key, value in self.webGadget.registerLamp.lampDict.items():

            addresses.append("http://{url}/lamp/status".format(url=value["ip"]))

        address = addresses[0]
        try:

            x = requests.get(address, timeout=20)
            response = x.json()

            logging.debug("StatusCode: {0}".format(x.status_code))

            if x.status_code == 200:
                logging.debug("Response: {0}".format(x.text))
                return response.get('status')
            else:
                logging.debug("Response: Failed, so the status faked as OFF")
                return 'off'


        # NewConnectionError
        # ConnectTimeoutError
        except Exception as e:
            logging.error("Exception: {0}. Status faked as OFF".format(e))
            return 'off'
