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

class Report:

    #   reportDict[
    #      "5": {"ip":"192.168.0.112", "record": [{"timestamp": 35779, "levelValue": 31, "levelVariance": 0.0, "temperatureValue": 20.1, "humidityValue": 20}, {}, {}] },
    #      "9": {"ip":"192.168.0.117", "record": [{"timestamp": 35787, "levelValue": 27, "levelVariance": 0.1, "temperatureValue": 20.1, "humidityValue": 20}, {}, {}] },
    #   ]

    def __init__(self, reportPath):

        self.lockReport = Lock()

        self.reportDict = {}
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

#                    print("lineArray: ", lineArray)

                    #{date}\t{levelId}\t{ip}\t{value}\t{variance}
                    dateString = lineArray[0]

                    dateTime = parser.parse(dateString).astimezone()

                    timeStamp = dateTime.timestamp() #datetime.fromtimestamp(value)
                    stationId = lineArray[1]
                    ip = lineArray[2]

                    try:
                        levelValue = float(lineArray[3])
                        levelVariance = float(lineArray[4])
                    except:
                        levelValue = None
                        levelVariance = None

                    try:
                        temperatureValue = float(lineArray[5])
                    except:
                        temperatureValue = None

                    try:
                        humidityValue = float(lineArray[6])
                    except:
                        humidityValue = None

                    if not stationId in self.reportDict:
                        self.reportDict[stationId] = {"ip": ip, "record": []}
                    self.reportDict[stationId]["record"].append({"timeStamp": timeStamp, "levelValue": levelValue, "levelVariance": levelVariance, "temperatureValue": temperatureValue, "humidityValue": humidityValue})

                except Exception as e:
                    continue

#            print("end line")
#            print()


    def getRawReportCopy(self):
        with self.lockReport:
            return deepcopy(self.reportDict)

    def addRecordLevel(self, dateString, stationId, ip, levelValue, levelVariance, temperatureValue, humidityValue):


        with self.lockReport:

            dateTime = parser.parse(dateString).astimezone()

            timeStamp = dateTime.timestamp()

            if not stationId in self.reportDict:
                self.reportDict[stationId] = {'ip': ip, 'record': []}
            self.reportDict[stationId]['record'].append({'timeStamp': timeStamp, 'levelValue': levelValue, 'levelVariance': levelVariance, 'temperatureValue': temperatureValue, 'humidityValue': humidityValue})

            with open(self.reportPath, 'a') as fileObject:
                fileObject.write("{dateString}{sep}{stationId}{sep}{ip}{sep}{levelValue}{sep}{levelVariance}{sep}{temperatureValue}{sep}{humidityValue}\n".format(dateString=dateString, stationId=stationId,ip=ip, levelValue=levelValue,levelVariance=levelVariance,temperatureValue=temperatureValue if temperatureValue else "", humidityValue=humidityValue if humidityValue else "", sep=self.separator))
