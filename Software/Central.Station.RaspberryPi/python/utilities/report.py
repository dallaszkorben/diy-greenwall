import logging

from dateutil import parser
from datetime import datetime

from scipy import stats

from copy import deepcopy

# ---------------------
# It needed
# Otherwise RuntimeError: main thread is not in main loop with Matplotlib and Flask
#import matplotlib
#matplotlib.use('Agg')
# --------------------

#import matplotlib.pyplot as plt
#import matplotlib.dates as md
#import numpy as np
#import pandas as pd

import time

from threading import Lock

#from scipy.signal import savgol_filter

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

#    def __init__(self, reportLevelPath, reportTemperaturePath):
    def __init__(self, reportPath):

#        self.lockReportLevel = Lock()
#        self.lockReportTemperature = Lock()
        self.lockReport = Lock()

#        self.reportLevelDict = {}
#        self.reportTemeratureList = []
        self.reportDict = {}

        self.reportPath = reportPath

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
#        with open(reportLevelPath, 'r') as fileObject:
        with open(self.reportPath, 'r') as fileObject:

            lines = fileObject.readlines()
            for line in lines:

                try:
                    lineArray = line.split()

                    #{date}\t{levelId}\t{ip}\t{value}\t{variance}
                    dateString = lineArray[0]

                    dateTime = parser.parse(dateString).astimezone()

                    timeStamp = dateTime.timestamp() #datetime.fromtimestamp(value)
                    stationId = lineArray[1]
                    ip = lineArray[2]
                    levelValue = float(lineArray[3])
                    levelVariance = float(lineArray[4])

                    try:
                        temperatureValue = float(lineArray[5])
                        humidityValue = float(lineArray[6])
                    except:
                        temperatureValue = None
                        humidityValue = None

#                    if not levelId in self.reportLevelDict:
#                        self.reportLevelDict[levelId] = {'ip': ip, 'record': []}
#                    self.reportLevelDict[levelId]['record'].append({'timeStamp': timeStamp, 'levelValue': levelValue, 'levelVariance': variance, 'temperatureValue': temperatureValue, 'humidityValue': humidityValue})

                    if not stationId in self.reportDict:
                        self.reportDict[stationId] = {"ip": ip, "record": []}
                    self.reportDict[stationId]["record"].append({"timeStamp": timeStamp, "levelValue": levelValue, "levelVariance": levelVariance, "temperatureValue": temperatureValue, "humidityValue": humidityValue})

                except Exception as e:
                    continue

#    def getRawReportLevelCopy(self):
#        with self.lockReportLevel:
#            return deepcopy(self.reportLevelDict)
    def getRawReportCopy(self):
        with self.lockReport:
            return deepcopy(self.reportDict)

    def addRecordLevel(self, dateString, stationId, ip, levelValue, levelVariance, temperatureValue, humidityValue):

#        with self.lockReportLevel:
        with self.lockReport:

            dateTime = parser.parse(dateString).astimezone()

            timeStamp = dateTime.timestamp()
#            if not stationId in self.reportLevelDict:
#                self.reportLevelDict[stationId] = {'ip': ip, 'record': []}
#            self.reportLevelDict[stationId]['record'].append({'timeStamp': timeStamp, 'levelValue': levelValue, 'levelVariance': levelVariance, 'temperatureValue': temperatureValue, 'humidityvalue': humidityValue})

            if not stationId in self.reportDict:
                self.reportDict[stationId] = {'ip': ip, 'record': []}
            self.reportDict[stationId]['record'].append({'timeStamp': timeStamp, 'levelValue': levelValue, 'levelVariance': levelVariance, 'temperatureValue': temperatureValue, 'humidityvalue': humidityValue})

            with open(self.reportPath, 'a') as fileObject:
                fileObject.write("{dateString}\t{stationId}\t{ip}\t{levelValue}\t{levelVariance}\t{temperatureValue}\t{humidityValue}\n".format(dateString=dateString, stationId=stationId,ip=ip, levelValue=levelValue,levelVariance=levelVariance,temperatureValue=temperatureValue if temperatureValue else "", humidityValue=humidityValue if humidityValue else ""))


#    def getRawReportTemperatureCopy(self):
#        with self.lockReportTempearture:
#            return deepcopy(self.reportTemperatureList)
#
#    def addRecordTemperature(self, dateString, temperature, humidity):
#
#        with self.lockReportTemperature:
#            dateTime = parser.parse(dateString).astimezone()
#
#            timeStamp = dateTime.timestamp()
#
#            self.reportTemperatureList.append({'timeStamp': timeStamp, 'temperature': temperature, 'humidity': humidity})










#    def filterReportLevelCopy(self, reportCopy, startDateStamp, endDateStamp=None):
#        """
#        return reportCopy
#        [
#              "5": {"ip":"192.168.0.112", "record": [{"timeStamp": 35779, "value": 31, "variance": 0.0}, {}, {}] },
#              "9": {"ip":"192.168.0.117", "record": [{"timeStamp": 35787, "value": 27, "variance": 0.1}, {}, {}] },
#        ]
#        """
#        # if NO endDateStamp provided
#        if endDateStamp == None:
#
#            # takes NOW as endDateStamp
#            endDateStamp = datetime.now().astimezone().timestamp()
#
#        for levelId in reportCopy:
#
#            for c in list(reportCopy[levelId]["record"]):
#                if c['timeStamp'] < startDateStamp or c['timeStamp'] > endDateStamp:
#                    reportCopy[levelId]['record'].remove(c)
#
#        return reportCopy
#
#    def smoothReportLevelCopy(self, reportCopy, window=15):
#        """
#        return reportCopy
#        [
#              "5": {"ip":"192.168.0.112", "record": [{"timeStamp": 35779, "value": 31, "variance": 0.0}, {}, {}] },
#              "9": {"ip":"192.168.0.117", "record": [{"timeStamp": 35787, "value": 27, "variance": 0.1}, {}, {}] },
#        ]
#        """
#        for levelId in reportCopy:
#            timeStamps = [r['timeStamp'] for r in reportCopy[levelId]["record"]]
#
#            # collect levels
#            values = [r['value'] for r in reportCopy[levelId]["record"]]
#
#            # smooth curve
#            newValues = self.smooth(values, min(window, len(values)))
#
#            for r, v in zip( reportCopy[levelId]["record"], newValues):
#                r.update({'value': v})
#
#            reportCopy[levelId]['record'] = reportCopy[levelId]['record'][window:]
#
#        return reportCopy
#
#
#
#    def calculateTrendForReportCopy(self, reportCopy):
#        """
#        return reportCopy
#            {
#              "5": {"ip":"192.168.0.112", "slope": -1.2, "intercept": 0.234, 'stdError': 0.002, "record": [{"timestamp": 35779, "date": "2021-11-12T21:12:22.12345+01:00", "value": 31, "variance": 0.0}, {}, {}] },
#              "9": {"ip":"192.168.0.117", "slope": 0.72, "intercept": 123.7, 'stdError': 0.021, "record": [{"timestamp": 35787, "date": "2021-11-12T21:12:25.34512+01:00", "value": 27, "variance": 0.1}, {}, {}] },
#            }
#        """
#        for levelId in reportCopy:
#
#            ip = reportCopy[levelId]['ip']
#
#            dataCollection = {'x': [], 'y': []}   # for trend
#
#            for record in reportCopy[levelId]['record']:
#                timeStamp = record['timeStamp']
#
#                value = float(record['value'])
#                variance = float(record['variance'])
#
#                dataCollection['x'].append(timeStamp)  # for trend
#                dataCollection['y'].append(value)      # for trend
#
#            # for trend
#            if len(dataCollection['x']) > 1:
#
#                slope, intercept = self.getRegression(dataCollection['x'], dataCollection['y'])
#            else:
#                slope = None
#                intercept = None
#
#            reportCopy[levelId]['slope'] = slope
#            reportCopy[levelId]['intercept'] = intercept
#
#        return reportCopy
#
#    def getGraphFromReportCopy(self, reportCopy, levelId=None):
#        retDict = {}
#
#        for actualLevelId in reportCopy:
#
#            if len(reportCopy[actualLevelId]['record']) == 0:
#                continue
#
#            if levelId and levelId != actualLevelId:
#                continue
#
##            print(reportCopy[actualLevelId])
#
#            slope = reportCopy[actualLevelId]['slope']
#            intercept = reportCopy[actualLevelId]['intercept']
#
#            recordList = reportCopy[actualLevelId]['record']
#            speedInmmPerDay = slope * 86400 # 60*60*24 => mm/day
#            speedInmmPerDayString = "{0:.1f} [mm/day]".format(speedInmmPerDay)
#
#            # Input
#            measure_timestamps = [record['timeStamp'] for record in recordList]
#            measure_dates = [datetime.fromtimestamp(ts) for ts in measure_timestamps]
#            measure_values = [record['value'] for record in recordList]
#
#            if len(measure_dates) > 1:
#                trend_dates = [measure_dates[0], measure_dates[-1]]
#                trend_values = [measure_timestamps[0] * slope + intercept, measure_timestamps[-1] * slope + intercept]
#            else:
#                trend_dates = []
#                trend_values = []
#
#            # clean plt
#            plt.clf()
#
#            plt.rcParams.update({'figure.autolayout': True})
#            plt.tight_layout()
#            #plt.subplots_adjust(bottom=0.30)
#
##            px = 1/plt.rcParams['figure.dpi'] # pixel in inches
# #           plt.subplots(figsize=(1200*px, 600*px))
#            plt.xticks(rotation=25)
#
#            plt.text(measure_dates[0], measure_timestamps[0] * slope + intercept, speedInmmPerDayString)
#
#            ax=plt.gca()
#
#            # configure tick locators
#            x_major_locator=md.DayLocator()
#            x_minor_locator=md.HourLocator(interval=1)
#            ax.xaxis.set_major_locator(x_major_locator)
#            ax.xaxis.set_minor_locator(x_minor_locator)
#
#            # format X values
#            #xfmt=md.DateFormatter('%Y-%m-%d %H:%M:%S')
#            xfmt=md.DateFormatter('%Y-%m-%d %H:%M')
#            ax.xaxis.set_major_formatter(xfmt)
#
#            ax.set(xlabel="time", ylabel='level [mm]', title=f'Sensor {actualLevelId}')
#            ax.grid()
#
#            plt.plot(measure_dates, measure_values, label="Measure", linewidth='1', color='green')
#            plt.plot(trend_dates, trend_values, label="Trend", linewidth='3', color='red')
#
#            plt.legend()
#
#            fileName = f'graph_{actualLevelId}.jpg'
#
#            retDict[actualLevelId] = fileName
#
#            logging.debug( "!!! Start saving" )
#
#            plt.savefig(fileName)
#
#            logging.debug( "!!! End saving." )
#
#        return retDict
#
#    def getGraphs(self, startDateStamp, endDateStamp=None, window=15):
#
##        logging.debug( "!!! - start copy !!!" )
#        reportCopy = self.getRawReportCopy()
##        logging.debug( "!!! - end copy. length: {0}!!!".format(len(reportCopy['6']['record']) ) )
#
##        logging.debug( "!!! - start filter !!!" )
#        self.filterReportCopy(reportCopy, startDateStamp)
##        logging.debug( "!!! - end filter !!!" )
#
##        logging.debug( "!!! - start smoothing !!!" )
#        self.smoothReportCopy(reportCopy, window=window)
##        logging.debug( "!!! - end smoothing !!!" )
#
##        logging.debug( "!!! - start trend !!!" )
#        self.calculateTrendForReportCopy(reportCopy)
##        logging.debug( "!!! - end trend. length: {0}!!!".format(len(reportCopy['6']['record']) ) )
#
#        logging.debug( "!!! - start graph !!!" )
#        ret = self.getGraphFromReportCopy(reportCopy, levelId=None)
#        logging.debug( "!!! - end graph !!!" )
#
#        return ret
#
#
#    def smooth(self, y, winsize=5):
#        return np.array(pd.Series(y).rolling(winsize).mean())
#
#    def getVariance(self, arr, mean):
#        return np.sum((arr-mean)**2)
#
#    def getCovariance(self, arr_x, mean_x, arr_y, mean_y):
#        final_arr = (arr_x-mean_x)*(arr_y-mean_y)
#        return np.sum(final_arr)
#
#    def getRegression(self, x, y):
#
#        x_mean = np.mean(x)
#        y_mean = np.mean(y)
#
#        m = self.getCovariance(x, x_mean, y, y_mean)/self.getVariance(x, x_mean)
#        b = y_mean - x_mean*m
#
#        return m, b