import logging

from dateutil import parser
from datetime import datetime

from copy import deepcopy

import time

from threading import Lock


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

    #   camStreamDict[
    #      "5": {"ip":"192.168.0.112", "timestamp": 35779, "streamUrl": "http://192.168.50.123:81/stream", "captureUrl": "http://192.168.50.123:80/capture" },
    #      "9": {"ip":"192.168.0.117", "timestamp": 35787, "streamUrl": "http://192.168.50.123:81/stream", "captureUrl": "http://192.168.50.123:80/capture" },
    #   ]

    def __init__(self, registerPath):

        self.lockRegister = Lock()

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
        '''

        with open(self.registerPath, 'r') as fileObject:

            lines = fileObject.readlines()

            for line in lines:

                try:
                    lineArray = line.split(self.separator)

                    dateString = lineArray[0]

                    dateTime = parser.parse(dateString).astimezone()

                    timeStamp = dateTime.timestamp() #datetime.fromtimestamp(value)
                    camId = lineArray[1]
                    camIp = lineArray[2]
                    streamUrl = lineArray[3]
                    captureUrl = lineArray[4]

                    self.camDict[camId] = {"ip": camIp, "timeStamp": timeStamp, "streamUrl": streamUrl, "captureUrl": captureUrl}

                except Exception as e:
                    continue

    def register(self, dateString, camIp, camId, streamUrl, captureUrl):

        with self.lockRegister:

            dateTime = parser.parse(dateString).astimezone()
	
            timeStamp = dateTime.timestamp()

            self.camDict[camId] = {"ip": camIp, "timeStamp": timeStamp, "streamUrl": streamUrl, "captureUrl": captureUrl}

            with open(self.registerPath, 'w') as fileObject:

                for key, value in self.camDict.items():

                    dateString = datetime.fromtimestamp(value['timeStamp']).astimezone().isoformat()

                    fileObject.write("{dateString}{sep}{camId}{sep}{camIp}{sep}{streamUrl}{sep}{captureUrl}{sep}\n".format(dateString=dateString, camId=key, camIp=value["ip"], streamUrl=value["streamUrl"], captureUrl=value["captureUrl"], sep=self.separator))

    def getValueList(self, capture=True, stream=False, camId=None ):
        output = []

        # TODO if the record is outdated: remove it from the list

        for ci, value in self.camDict.items():

            if not camId or (camId==ci):
                camIp=value['ip']
                streamUrl=value['streamUrl']
                captureUrl=value['captureUrl']
                dateString = value['timeStamp']

                app = {"camId": ci}
                if capture:
                    app["captureUrl"] = captureUrl

                if stream:
                    app["streamUrl"] = streamUrl

                output.append(app)

#                output.append({"camId": si, "capIp": camIp, "streamUrl": streamUrl, "captureUrl": captureUrl,"timeStamp": dateString   })
        return output

#    def getRawReportCopy(self):
#        with self.lockReport:
#            return deepcopy(self.camDict)
