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

class RegisterPump:

    #   reportDict[
    #      "5": {"ip":"192.168.0.112", "timestamp": 35779 },
    #      "9": {"ip":"192.168.0.117", "timestamp": 35787 },
    #   ]

    def __init__(self, reportPath):

        self.lockRegister = Lock()

        self.pumpDict = {}
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
        with open(self.reportPath, 'w+') as fileObject:
            pass

        with open(self.reportPath, 'r') as fileObject:

            lines = fileObject.readlines()
            for line in lines:

                try:
                    lineArray = line.split(self.separator)

                    #{date}\t{levelId}\t{ip}\t{value}\t{variance}
                    dateString = lineArray[0]

                    dateTime = parser.parse(dateString).astimezone()

                    timeStamp = dateTime.timestamp() #datetime.fromtimestamp(value)
                    pumpId = lineArray[1]
                    ip = lineArray[2]

                    #if not pumpId in self.pumpDict:
                    self.pumpDict[pumpId] = {"ip": ip, "timeStamp": timeStamp}

                except Exception as e:
                    continue

    def register(self, dateString, pumpId, ip):

        with self.lockRegister:

            dateTime = parser.parse(dateString).astimezone()

            timeStamp = dateTime.timestamp()

            self.pumpDict[pumpId] = {"ip": ip, "timeStamp": timeStamp}

            with open(self.reportPath, 'w') as fileObject:

                for key, value in self.pumpDict.items():

                    dateString = datetime.fromtimestamp(value['timeStamp']).astimezone().isoformat()

                    fileObject.write("{dateString}{sep}{pumpId}{sep}{ip}{sep}\n".format(dateString=dateString, pumpId=key,ip=value["ip"], sep=self.separator))








#    def getLatestValues(self, stationId=None):
#        output = []
#        for si, value in self.reportDict.items():
#
#            if not stationId or (stationId==si):
#                ip=value['ip']
#                lastRecord = value['record'][-1]
#                output.append({"stationId": si, "ip": ip, "timeStamp": lastRecord['timeStamp'], "levelValue": lastRecord['levelValue'], "temperatureValue":lastRecord['temperatureValue'], "humidityValue": lastRecord['humidityValue']   })
#        return output

