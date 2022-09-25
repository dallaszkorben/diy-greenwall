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

class RegisterCam:

    #   camDict[
    #      "5": {"ip":"192.168.0.26", "timestamp": 35779, "configureUrl": "http://192.168.0.26:80/configure", "streamUrl": "http://192.168.0.26:81/stream", "captureUrl": "http://192.168.0.26:80/capture" },
    #      "9": {"ip":"192.168.0.27", "timestamp": 35787, "configureUrl": "http://192.168.0.27:80/configure", "streamUrl": "http://192.168.0.27:81/stream", "captureUrl": "http://192.168.0.27:80/capture" },
    #   ]

    def __init__(self,  web_gadget, registerPath):

        self.lockRegister = Lock()

        self.web_gadget = web_gadget
        self.camDict = {}
        self.registerPath = registerPath

        self.separator = ";"

        #
        # Fill up camDict
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
        I do not register the values in the cam_register.log when I start the Control Box
        When the Control Box starts, then every registered cam should be deleted
        If any camera is connected, then in some seconds it will be registered anyway
        '''
        with self.lockRegister:
            open(self.registerPath, 'w').close()

        x = threading.Thread(target=self.cleanRegister, args=())
        x.start()

    def getCamDictValueByIp(self, ip):
        """
        Gives back the values of the registered camera by its IP
        If the camera is not registered then it gives back None
        The returned value is a dict like this:
            {"ip":"192.168.0.26", "timestamp": 35779, "configureUrl": "http://192.168.0.26:80/configure", "streamUrl": "http://192.168.0.26:81/stream", "captureUrl": "http://192.168.0.26:80/capture" }
        """
        with self.lockRegister:

            value = None
            for camId, value in self.camDict.items():
                if value["ip"] == ip:
                    value = self.camDict[camId]
                    break
            return value

    def getCamDictValue(self, camId):
        """
        Gives back the values of the registered camera by its camId
        If the camera is not registered then it gives back None
        The returned value is a dict like this:
            {"ip":"192.168.0.26", "timestamp": 35779, "configureUrl": "http://192.168.0.26:80/configure", "streamUrl": "http://192.168.0.26:81/stream", "captureUrl": "http://192.168.0.26:80/capture" }
        """
        with self.lockRegister:

            if camId in self.camDict:
                value=self.camDict[camId]
                return value
            else:
                return None

    def cleanRegister(self):
        """
        I delete every recorded cam from the cam_register.log file
        I delete every record from self.camDict which is older than self.timingCamLateRegisterTimeLimit (120s) 
            [timing]
            cam-late-register-time-limit_seconds = 120
        """

        while True:
            logging.debug("Cam Register Check - Start to check")

            with self.lockRegister:
#                dateTime = parser.parse(dateString).astimezone()
#                timeStamp = dateTime.timestamp()
                dateNow = datetime.now().astimezone().isoformat()

                # delete every record from the self.camDict which is older than self.timingCamLateRegisterTimeLimit
                # needs copy() otherwise: "RuntimeError: dictionary changed size during iteration" 
                for key, value in self.camDict.copy().items():
                    dateLimit = (datetime.fromtimestamp(value['timeStamp']) + timedelta(seconds=int(self.web_gadget.timingCamLateRegisterTimeLimit))).astimezone().isoformat()

                    # if the record is too old
                    if dateNow > dateLimit:
                        self.camDict.pop(key)

                # delete every record from cam_register.log
                with open(self.registerPath, 'w') as fileObject:

                    logging.error("   Clear the cam_register.log file")

                    for key, value in self.camDict.copy().items():
                        dateString = datetime.fromtimestamp(value['timeStamp']).astimezone().isoformat()
                        fileObject.write("{dateString}{sep}{camId}{sep}{camIp}{sep}{configureUrl}{sep}{captureUrl}{sep}{streamUrl}{sep}\n".format(dateString=dateString, camId=key, camIp=value["ip"], configureUrl=value["configureUrl"], streamUrl=value["streamUrl"], captureUrl=value["captureUrl"], sep=self.separator))


                        logging.error("   Add key to cam_register.log: " + key)


            logging.debug("Cam Register Check - Waiting 70 sec for the next check")

            time.sleep(70)

    def register(self, dateString, camIp, camId, configureUrl, streamUrl, captureUrl):
        """
        Registers the camera in the cam_register.log and in the self.camDict dictionary
        """
        with self.lockRegister:

            dateTime = parser.parse(dateString).astimezone()
            timeStamp = dateTime.timestamp()

#            dateNow = datetime.now().astimezone().isoformat()
#
#            # delete every record from the self.camDict which is older than self.timingCamLateRegisterTimeLimit
#            for key, value in self.camDict.items():
#                #recordDate = datetime.fromtimestamp(value['timeStamp']).astimezone().isoformat()
#                dateLimit = (datetime.fromtimestamp(value['timeStamp']) + timedelta(seconds=int(self.web_gadget.timingCamLateRegisterTimeLimit))).astimezone().isoformat()
#
#                logging.error("!!!!")
#                logging.error("dateNow: " + dateNow + " - dateLimit: " + dateLimit)
#                logging.error("!!!!")
#
#                # if the record is too old
#                if dateNow > dateLimit:
#                    self.camDict.pop(key)

            # delete every record from cam
            # register the cam - if it exists then updates
            self.camDict[camId] = {"ip": camIp, "timeStamp": timeStamp, "configureUrl": configureUrl, "streamUrl": streamUrl, "captureUrl": captureUrl}
            with open(self.registerPath, 'w') as fileObject:
                for key, value in self.camDict.items():
                    dateString = datetime.fromtimestamp(value['timeStamp']).astimezone().isoformat()
                    fileObject.write("{dateString}{sep}{camId}{sep}{camIp}{sep}{configureUrl}{sep}{captureUrl}{sep}{streamUrl}{sep}\n".format(dateString=dateString, camId=key, camIp=value["ip"], configureUrl=value["configureUrl"], streamUrl=value["streamUrl"], captureUrl=value["captureUrl"], sep=self.separator))

    def getValueList(self, configure=False, capture=True, stream=False, camId=None ):
        output = []

        # TODO if the record is outdated: remove it from the list

        for ci, value in self.camDict.items():

            if not camId or (camId==ci):
                camIp=value['ip']
                configureUrl=value['configureUrl']
                streamUrl=value['streamUrl']
                captureUrl=value['captureUrl']
                dateString = value['timeStamp']

                app = {"camId": ci}
                if configure:
                    app["configureUrl"] = configureUrl

                if capture:
                    app["captureUrl"] = captureUrl

                if stream:
                    app["streamUrl"] = streamUrl

                output.append(app)

#                output.append({"camId": si, "capIp": camIp, "configureUrl": configureUrl, "streamUrl": streamUrl, "captureUrl": captureUrl,"timeStamp": dateString   })
        return output

#    def getRawReportCopy(self):
#        with self.lockReport:
#            return deepcopy(self.camDict)
