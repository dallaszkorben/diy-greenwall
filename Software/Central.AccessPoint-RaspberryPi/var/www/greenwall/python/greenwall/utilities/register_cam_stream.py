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

class RegisterCamStream:

    #   camStreamDict[
    #      "5": {"ip":"192.168.0.112", "timestamp": 35779, "url": "http://192.168.50.123:81/stream" },
    #      "9": {"ip":"192.168.0.117", "timestamp": 35787, "url": "http://192.168.50.124:81/stream" },
    #   ]

    def __init__(self, reportPath):

        self.lockRegister = Lock()

        self.camStreamDict = {}
        self.reportPath = reportPath

        self.separator = ";"

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
        with open(self.reportPath, 'r') as fileObject:

            lines = fileObject.readlines()


            for line in lines:

                try:
                    lineArray = line.split(self.separator)

                    #{date}\t{levelId}\t{ip}\t{value}\t{variance}
                    dateString = lineArray[0]

                    dateTime = parser.parse(dateString).astimezone()

                    timeStamp = dateTime.timestamp() #datetime.fromtimestamp(value)
                    camStreamId = lineArray[1]
                    camStreamIp = lineArray[2]
                    camStreamUrl = lineArray[3]

                    #if not lampId in self.lampDict:
                    self.camStreamDict[camStreamId] = {"ip": camStreamIp, "timeStamp": timeStamp, "url": camStreamUrl}

                except Exception as e:
                    continue



    def register(self, dateString, camStreamIp, camStreamId, camStreamUrl):

        with self.lockRegister:

            dateTime = parser.parse(dateString).astimezone()

            timeStamp = dateTime.timestamp()

            self.camStreamDict[camStreamId] = {"ip": camStreamIp, "timeStamp": timeStamp, "url": camStreamUrl}

            with open(self.reportPath, 'w') as fileObject:

                for key, value in self.camStreamDict.items():

                    dateString = datetime.fromtimestamp(value['timeStamp']).astimezone().isoformat()

                    fileObject.write("{dateString}{sep}{camStreamId}{sep}{camStreamIp}{sep}{camStreamUrl}{sep}\n".format(dateString=dateString, camStreamId=key, camStreamIp=value["ip"], camStreamUrl=value["url"], sep=self.separator))








    def getValueList(self, camStreamId=None):
        output = []

        for si, value in self.camStreamDict.items():

            if not camStreamId or (camStreamId==si):
                camStreamIp=value['ip']
                camStreamUrl=value['url']
                dateString = value['timeStamp']
                output.append({"id": si, "ip": camStreamIp, "url": camStreamUrl,"timeStamp": dateString   })
        return output

#    def getRawReportCopy(self):
#        with self.lockReport:
#            return deepcopy(self.camStreamDict)
