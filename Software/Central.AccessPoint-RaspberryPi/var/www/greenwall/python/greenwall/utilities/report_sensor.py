import logging

from dateutil import parser
from datetime import datetime

from copy import deepcopy

import time

from threading import Lock

class ReportSensor:

    #   reportDict[
    #      "5": {"ip":"192.168.0.112", "record": [{"timestamp": 35779, "levelValue": 31, "temperatureValue": 20.1, "humidityValue": 20, "pressureValue": 123}, {}, {}] },
    #      "9": {"ip":"192.168.0.117", "record": [{"timestamp": 35787, "levelValue": 27, "temperatureValue": 20.1, "humidityValue": 20, "pressureValue": 123}, {}, {}] },
    #   ]

    def __init__(self, reportPath):

        self.lockReport = Lock()

        self.reportDict = {}
        self.reportPath = reportPath

        self.separator = ";"

        #
        # Fill up the reportDict
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
        with open(self.reportPath, 'r') as fileObject:

            lines = fileObject.readlines()
            for line in lines:

                try:

                    #{date}\t{levelId}\t{ip}\t{level}\t{temperature}\t{humidity}\t{pressure}
                    lineArray = line.split(self.separator)

                    dateString = lineArray[0]

                    dateTime = parser.parse(dateString).astimezone()

                    timeStamp = dateTime.timestamp() #datetime.fromtimestamp(value)
                    stationId = lineArray[1]
                    ip = lineArray[2]

                    try:
                        levelValue = float(lineArray[3])
                    except:
                        levelValue = None

                    try:
                        temperatureValue = float(lineArray[4])
                    except:
                        temperatureValue = None

                    try:
                        humidityValue = float(lineArray[5])
                    except:
                        humidityValue = None

                    try:
                        pressureValue = float(lineArray[6])
                    except:
                        pressureValue = None

                    if not stationId in self.reportDict:
                        self.reportDict[stationId] = {"ip": ip, "record": []}
                    self.reportDict[stationId]["record"].append({"timeStamp": timeStamp, "levelValue": levelValue, "temperatureValue": temperatureValue, "humidityValue": humidityValue, "pressureValue": pressureValue})

                except Exception as e:
                    continue

    def getLatestValues(self, stationId=None):
        output = []
        for si, value in self.reportDict.items():

            if not stationId or (stationId==si):
                ip=value['ip']
                lastRecord = value['record'][-1]
                output.append({"stationId": si, "ip": ip, "timeStamp": lastRecord['timeStamp'], "levelValue": lastRecord['levelValue'], "temperatureValue":lastRecord['temperatureValue'], "humidityValue": lastRecord['humidityValue'], "pressureValue": lastRecord['pressureValue'] })
        return output

    def getRawReportCopy(self):
        with self.lockReport:
            return deepcopy(self.reportDict)

    def addRecordSensor(self, dateString, stationId, ip, levelValue, temperatureValue, humidityValue, pressureValue):

        with self.lockReport:

            dateTime = parser.parse(dateString).astimezone()

            timeStamp = dateTime.timestamp()

            if not stationId in self.reportDict:
                self.reportDict[stationId] = {'ip': ip, 'record': []}
            self.reportDict[stationId]['record'].append({'timeStamp': timeStamp, 'levelValue': levelValue, 'temperatureValue': temperatureValue, 'humidityValue': humidityValue, 'pressureValue': pressureValue})

            with open(self.reportPath, 'a') as fileObject:
                fileObject.write("{dateString}{sep}{stationId}{sep}{ip}{sep}{levelValue}{sep}{temperatureValue}{sep}{humidityValue}{sep}{pressureValue}\n".format(dateString=dateString, stationId=stationId,ip=ip, levelValue=levelValue if levelValue else "", temperatureValue=temperatureValue if temperatureValue else "", humidityValue=humidityValue if humidityValue else "", pressureValue=pressureValue if pressureValue else "", sep=self.separator))


