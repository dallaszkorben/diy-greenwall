import logging
import threading
import time
from threading import Lock

from dateutil import parser
from datetime import datetime, timedelta

from copy import deepcopy

# from datetime import datetime
# from dateutil import parser
#
# datetime now()
#  datetime.datetime.now().astimezone()
#
# String now()
#  datetime.datetime.now().astimezone().isoformat()
#
# datetime from String
#    date = parser.parse(dateString)
#
# timestamp from datetime
#    timeStamp = date.timestamp()
#    timeStamp = datetime.timestamp(date)
#
# datetime from timestamp
#    datetime.fromtimestamp(timeStamp)
#

class RegisterSensor:

    #   sensorDict[
    #      "5": {"ip":"192.168.0.26", "timestamp": 35779, "configureUrl": "http://192.168.0.26:80/configure", "measureActualUrl": "http://192.168.0.26:80/all/actual", "collectAverageUrl": "http://192.168.0.26:80/all/aggregate" },
    #      "9": {"ip":"192.168.0.27", "timestamp": 35779, "configureUrl": "http://192.168.0.27:80/configure", "measureActualUrl": "http://192.168.0.27:80/all/actual", "collectAverageUrl": "http://192.168.0.27:80/all/aggregate" },
    #   ]

    def __init__(self,  web_gadget, registerPath):

        self.lockRegister = Lock()

        self.web_gadget = web_gadget
        self.sensorDict = {}
        self.registerPath = registerPath

        self.separator = ";"

        #
        # Fill up sensorDict
        #
        # TODO 'r' is not correct because if the file does not exist, an exception will be raised
        # TODO 'w+' does not work either
        #
        '''
        w  write mode
        r  read mode
        a  append mode

        w+  create file if it doesn't exist and open it in write mode
        r+  open for reading and writing. Does not create file.
        a+  create file if it doesn't exist and open it in append mode

        The concept has changed.
        I do not register the values in the sensor_register.log when I start the Control Box
        When the Control Box starts, then every registered sensor should be deleted
        If any sensor station is connected, then in some seconds it will be registered anyway
        '''
        with self.lockRegister:
            open(self.registerPath, 'w').close()

        x = threading.Thread(target=self.cleanRegister, args=())
        x.start()

    def getSensorDictValueByIp(self, ip):
        """
        Gives back the values of the registered sensor by its IP
        If the sensor station is not registered then it gives back None
        The returned value is a dict like this:
            {"ip":"192.168.0.27", "timestamp": 35779, "configureUrl": "http://192.168.0.27:80/configure", "measureActualUrl": "http://192.168.0.27:80/all/actual", "collectAverageUrl": "http://192.168.0.27:80/all/aggregate" }
        """
        with self.lockRegister:

            value = None
            for stationId, value in self.sensorDict.items():
                if value["ip"] == ip:
                    value = self.sensorDict[stationId]
                    break
            return value

    def getSensorDictValueById(self, stationId):
        """
        Gives back the values of the registered sensor by its stationId
        If the sensor station is not registered then it gives back None
        The returned value is a dict like this:
            {"ip":"192.168.0.27", "timestamp": 35779, "configureUrl": "http://192.168.0.27:80/configure", "measureActualUrl": "http://192.168.0.27:80/all/actual", "collectAverageUrl": "http://192.168.0.27:80/all/aggregate" }
        """
        with self.lockRegister:

            if stationId in self.sensorDict:
                value=self.sensorDict[stationId]
                return value
            else:
                return None

    def cleanRegister(self):
        """
        I delete every recorded sensor from the sensor_register.log file
        I delete every record from self.sensorDict which is older than self.timingSensorLateRegisterTimeLimit (120s) 
            [timing]
            sensor-late-register-time-limit_seconds = 120
        """

        while True:
            logging.debug("Sensor Register Check - Start to check")

            with self.lockRegister:
#                dateTime = parser.parse(dateString).astimezone()
#                timeStamp = dateTime.timestamp()
                dateNow = datetime.now().astimezone().isoformat()

                # delete every record from the self.sensorDict which is older than self.timingSensorLateRegisterTimeLimit
                # needs copy() otherwise: "RuntimeError: dictionary changed size during iteration" 
                for key, value in self.sensorDict.copy().items():
                    dateLimit = (datetime.fromtimestamp(value['timeStamp']) + timedelta(seconds=int(self.web_gadget.timingSensorLateRegisterTimeLimit))).astimezone().isoformat()

                    # if the record is too old
                    if dateNow > dateLimit:
                        self.sensorDict.pop(key)

                # delete every record from sensor_register.log
                with open(self.registerPath, 'w') as fileObject:

                    logging.debug("   Clear the sensor_register.log file")

                    for key, value in self.sensorDict.copy().items():
                        dateString = datetime.fromtimestamp(value['timeStamp']).astimezone().isoformat()
                        fileObject.write("{dateString}{sep}{stationId}{sep}{stationIp}{sep}{configureUrl}{sep}{measureActualUrl}{sep}{collectAverageUrl}{sep}\n".format(dateString=dateString, stationId=key, stationIp=value["ip"], configureUrl=value["configureUrl"], measureActualUrl=value["measureActualUrl"], collectAverageUrl=value["collectAverageUrl"], sep=self.separator))

                        logging.debug("   Add key to sensor_register.log: " + key)


            logging.debug("Sensor Register Check - Waiting 70 sec for the next check")

            time.sleep(70)

    def register(self, dateString, stationIp, stationId, configureUrl, measureActualUrl, collectAverageUrl, triggerReportUrl):
        """
        Registers the station in the sensor_register.log and in the self.sensorDict dictionary
        """
        with self.lockRegister:

            dateTime = parser.parse(dateString).astimezone()
            timeStamp = dateTime.timestamp()

            # register the sensor - if it exists then updates
            self.sensorDict[stationId] = {"ip": stationIp, "timeStamp": timeStamp, "configureUrl": configureUrl, "measureActualUrl": measureActualUrl, "collectAverageUrl": collectAverageUrl, "triggerReportUrl": triggerReportUrl}
            with open(self.registerPath, 'w') as fileObject:
                for key, value in self.sensorDict.items():
                    dateString = datetime.fromtimestamp(value['timeStamp']).astimezone().isoformat()
                    fileObject.write("{dateString}{sep}{stationId}{sep}{stationIp}{sep}{configureUrl}{sep}{measureActualUrl}{sep}{collectAverageUrl}{sep}\n".format(dateString=dateString, stationId=key, stationIp=value["ip"], configureUrl=value["configureUrl"], measureActualUrl=value["measureActualUrl"], collectAverageUrl=value["collectAverageUrl"], sep=self.separator))

    def getValueList(self, configure=False, measureActual=False, collectAverage=False, triggerReport=False, stationId=None ):
        output = []

        # TODO if the record is outdated: remove it from the list

        for ci, value in self.sensorDict.items():

            if not stationId or (stationId==ci):
                stationIp=value['ip']
                configureUrl=value['configureUrl']
                measureActualUrl=value['measureActualUrl']
                collectAverageUrl=value['collectAverageUrl']
                triggerReportUrl=value['triggerReportUrl']
                dateString = value['timeStamp']

                app = {"stationId": ci}
                app["stationIp"] = stationIp

                if configure:
                    app["configureUrl"] = configureUrl

                if measureActual:
                    app["measureActualUrl"] = measureActualUrl

                if collectAverage:
                    app["collectAverageUrl"] = collectAverageUrl

                if triggerReport:
                    app["triggerReportUrl"] = triggerReportUrl

                output.append(app)

        return output


#    def getRawReportCopy(self):
#        with self.lockReport:
#            return deepcopy(self.sensorDict)
