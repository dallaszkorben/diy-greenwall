import requests
import logging
from datetime import datetime

class Lamp:

    def __init__(self, web_gadget):

        self.webGadget = web_gadget

    def turnLampOn(self, ip, lengthInSec=0):

        logging.debug("Turn on {0} lamp".format(ip))

        for key, value in self.webGadget.registerLamp.lampDict.items():

            current_ip = value["ip"]
            logging.debug("  try {0}".format(current_ip))

            if current_ip == ip:
                address = "http://{url}/lamp/on?lengthInSec={lengthInSec}".format(url=value["ip"], lengthInSec=lengthInSec)
                data = {'lengthInSec': lengthInSec}

                try:
                    x = requests.post(address, timeout=20)
                    logging.debug("StatusCode: {0}".format(x.status_code))

                # NewConnectionError
                # ConnectTimeoutError
                except Exception as e:
                    logging.error("Exception: {0}".format(e))

                break

            else:
                logging.debug("  Not this lamp")

    def turnLampOff(self, ip, lengthInSec=0):

        logging.debug("Turn off {0} lamp".format(ip))

        for key, value in self.webGadget.registerLamp.lampDict.items():

            current_ip = value["ip"]
            logging.debug("  try {0}".format(current_ip))

            if current_ip == ip:
                address = "http://{url}/lamp/off?lengthInSec={lengthInSec}".format(url=value["ip"], lengthInSec=lengthInSec)
                data = {'lengthInSec': lengthInSec}

                try:
                    x = requests.post(address, timeout=20)
                    logging.debug("StatusCode: {0}".format(x.status_code))

                # NewConnectionError
                # ConnectTimeoutError
                except Exception as e:
                    logging.error("Exception: {0}".format(e))

                break

            else:
                logging.debug("    Not this lamp")


    def getLampStatus(self, ip):

        #addresses = []
        address = ""

        actDateTime = datetime.now().astimezone()
        actTimeStamp = datetime.timestamp(actDateTime)

        # TODO later I should handle more lamps. Now works only one
        for key, value in self.webGadget.registerLamp.lampDict.items():


            current_ip = value["ip"]
            regTimeStamp = value["timeStamp"]
            diffSec = (actTimeStamp - regTimeStamp)

            # if less than 120 seconds was re-registering
            if ip == current_ip and diffSec < 120:
                # addresses.append("http://{url}/lamp/status".format(url=value["ip"]))
                address= "http://{url}/lamp/status".format(url=value["ip"])
                break

        try:

#            address = addresses[0]

            x = requests.get(address, timeout=20)
            response = x.json()

            logging.debug("Lamp StatusCode: {0}".format(x.status_code))

            if x.status_code == 200:
                logging.debug("Lamp Status Response: {0}".format(x.text))
                return  {"status": response.get('status')}
            else:
                logging.error("Lamp Status Response: Failed. Status is n/a")
                return {"status": "n/a"}


        # NewConnectionError
        # ConnectTimeoutError
        except Exception as e:

            if len(address) == 0:
                logging.debug("No lamp registered.")
            else:
                logging.error("Exception: {0}. Status is n/a".format(e))
            return {"status": "n/a"}


    def getLampList(self):

        response = []
        for key, value in self.webGadget.registerLamp.lampDict.items():

            lamp_id = key
            lamp_ip = value["ip"]
            timeStamp = value["timeStamp"]

            record = {'lamp_id': lamp_id, 'lamp_ip': lamp_ip, 'timeStamp': timeStamp}
            response.append(record)

        return response
