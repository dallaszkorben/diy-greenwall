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



    def triggerReport(self, stationId=None):

        # TODO: If stationId is not None, it must be handled. No loop in config, only pickup the one which matches with stationId

        response = {}

#        config = self.webGadget.registerSensor.getValueList(stationId=stationId, triggerReport=True)
        config = self.webGadget.registerSensor.getValueList(stationId=stationId, collectAverage=True)

        if(config):
            for stat in config:

                stationId = stat["stationId"]
                collectAverageUrl = stat["collectAverageUrl"]
                logging.debug("Try to fetch {0} station's average values from: {1}".format(stationId, collectAverageUrl))

                # --- solution with GET average values ---
                # --- Plan A ---

                try:
                    # stream=True => needed for the response.raw._connection.sock.getpeername()
                    x = requests.get(collectAverageUrl, timeout=20, stream=True)
                    ip = x.raw._connection.sock.getpeername()[0]

                    logging.debug("   StatusCode: {0}".format(x.status_code))

                    if x.status_code == 200:
                        logging.debug("   Response: {0}".format(x.text))

                        dateString = datetime.now().astimezone().isoformat()

                        response = x.json()
                        #{"success":true,"status":"OK","message":"OK","data":{"temperature":"22.90","humidity":"57.73","pressure":"101398.11","distance":"3.63"}}

                        levelValue = response['data']['distance']
                        temperatureValue = response['data']['temperature']
                        humidityValue = response['data']['humidity']
                        pressureValue = response['data']['pressure']

                        self.webGadget.reportSensor.addRecordSensor(dateString, stationId, ip, levelValue, temperatureValue, humidityValue, pressureValue)

                    else:
                        logging.error("   Response: Failed. Status is n/a")
                        response = {"status": "ERROR", "message": "When sending request 'GET {0}' to the sensor station {1} wrong status received: {2}.".format(collectAverageUrl, stationId, x.status_code)}

                # NewConnectionError
                # ConnectTimeoutError
                except Exception as e:
                    logging.error("   Exception: {0}".format(e))
                    response = {"status": "ERROR", "message": "Exception while sending request 'GET {0}' to the sensor station {1}: {2}.".format(collectAverageUrl, stationId, e)}


#                # --- solution with POST trigger ---
#                # --- Plan B ---
#                triggerReportUrl = stat["triggerReportUrl"]
#
#                logging.debug("Try to fetch {0} station's triggerReport from: {1}".format(stationId, triggerReportUrl))
#                try:
#
#                    x = requests.post(triggerReportUrl, timeout=20)
#                    response = x.json()
#
#                    logging.debug("   StatusCode: {0}".format(x.status_code))
#
#                    if x.status_code == 200:
#                        logging.debug("   Response: {0}".format(x.text))
#                    else:
#                        logging.error("   Response: Failed. Status is n/a")
#                        response = {"status": "ERROR", "message": "When sending request 'POST {0}' to the sensor station {1} wrong status received: {2}.".format(triggerReportUrl, stationId, x.status_code)}

                # NewConnectionError
                # ConnectTimeoutError
                except Exception as e:
                    logging.error("   Exception: {0}".format(e))
                    response = {"status": "ERROR", "message": "Exception while sending request 'POST {0}' to the sensor station {1}: {2}.".format(triggerReportUrl, stationId, e)}


        else:
            response = {"status": "ERROR", "message": "NO registered stationId '{0}' exists.".format(stationId)}

        return response
