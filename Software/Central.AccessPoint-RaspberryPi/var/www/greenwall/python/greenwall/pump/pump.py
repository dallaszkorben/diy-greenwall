import requests
import logging
from datetime import datetime


class Pump:

    def __init__(self, web_gadget):

        self.webGadget = web_gadget

    def turnPumpOn(self, ip, lengthInSec=0):

        logging.debug("Turn on {0} pump".format(ip))

        for key, value in self.webGadget.registerPump.pumpDict.items():

            current_ip = value["ip"]
            logging.debug("  try {0}".format(current_ip))

            if current_ip == ip:
                address = "http://{url}/pump/on?lengthInSec={lengthInSec}".format(url=value["ip"], lengthInSec=lengthInSec)
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
                logging.debug("  Not this pump")


    def turnPumpOff(self, ip):

        logging.debug("Turn off {0} pump".format(ip))

        for key, value in self.webGadget.registerPump.pumpDict.items():

            current_ip = value["ip"]
            logging.debug("  try {0}".format(current_ip))

            if current_ip == ip:

                address = "http://{url}/pump/off".format(url=value["ip"])

                try:
                    x = requests.post(address, timeout=20)
                    logging.debug("StatusCode: {0}".format(x.status_code))

                except Exception as e:
                    logging.error("Exception: {0}".format(e))

                break

            else:
                logging.debug("    Not this pump")


    def getPumpStatus(self, ip):

        address = ""

        actDateTime = datetime.now().astimezone()
        actTimeStamp = datetime.timestamp(actDateTime)

        for key, value in self.webGadget.registerPump.pumpDict.items():

            current_ip = value["ip"]
            regTimeStamp = value["timeStamp"]
            diffSec = (actTimeStamp - regTimeStamp)

            # if less than 120 seconds was re-registering
            if ip == current_ip and diffSec < 120:
                address = "http://{url}/pump/status".format(url=value["ip"])
                break

        try:

            x = requests.get(address, timeout=20)
            response = x.json()

            logging.debug("Pump StatusCode: {0}".format(x.status_code))

            if x.status_code == 200:
                logging.debug("Pump Status Response: {0}".format(x.text))

                st = response.get('status')
                cd = response.get('count-down')
                pt = response.get('percentage')

                result = {"status": st, "count-down": cd, "percentage": pt}
                return result

            else:
                logging.error("Pump Status Response: Failed. Status is n/a")

                result = {"status": "n/a", "count-down": 0, "percentage": 0}
                return result

        # NewConnectionError
        # ConnectTimeoutError
        except Exception as e:

            if len(address) == 0:
                logging.error("No pump registered.")
            else:
                logging.error("Exception: {0}. Status is n/a".format(e))

                result = {"status": "n/a", "count-down": 0, "percentage": 0}
                return result


    def getPumpList(self):

        response = []
        for key, value in self.webGadget.registerPump.pumpDict.items():

            pump_id = key
            pump_ip = value["ip"]
            timeStamp = value["timeStamp"]

            record = {'pump_id': pump_id, 'pump_ip': pump_ip, 'timeStamp': timeStamp}
            response.append(record)

        return response
