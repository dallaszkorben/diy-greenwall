import requests
import logging
from datetime import datetime

class Sensor:

    def __init__(self, web_gadget):

        self.webGadget = web_gadget

    def getAverage(self, stationId):
        response = {}

        config = self.webGadget.registerSensor.getValueList(stationId=stationId, collectAverage=True)
        if(config):
            collectAverageUrl = config[0]["collectAverageUrl"]

            logging.debug("Try to fetch {0} station's collectAverageUrl from: {1}".format(stationId, collectAverageUrl))
            try:

                x = requests.get(collectAverageUrl, timeout=20)
                response = x.json()

                logging.debug("   StatusCode: {0}".format(x.status_code))

                if x.status_code == 200:
                    logging.debug("   Response: {0}".format(x.text))
#                    result = response
                else:
                    logging.error("   Response: Failed. Status is n/a")
                    response = {"status": "ERROR", "message": "When sending request 'GET {0}' to the sensor station {1} wrong status received: {2}.".format(collectAverageUrl, stationId, x.status_code)}


            # NewConnectionError
            # ConnectTimeoutError
            except Exception as e:
                logging.error("   Exception: {0}".format(e))
                response = {"status": "ERROR", "message": "Exception while sending request 'GET {0}' to the sensor station {1}: {2}.".format(collectAverageUrl, stationId, e)}

        else:
            response = {"status": "ERROR", "message": "NO registered stationId '{0}' exists.".format(stationId)}

        return response
