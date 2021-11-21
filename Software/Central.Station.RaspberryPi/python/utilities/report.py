import logging

from dateutil import parser
from datetime import datetime

from scipy import stats

from copy import deepcopy

# ---------------------
# It needed
# Otherwise RuntimeError: main thread is not in main loop with Matplotlib and Flask
import matplotlib
matplotlib.use('Agg')
# --------------------

import matplotlib.pyplot as plt
import matplotlib.dates as md
import numpy as np
import pandas as pd

import time

from threading import Lock

#from scipy.signal import savgol_filter

# from datetime import datetime
# from dateutil import parser
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
    #      "5": {"ip":"192.168.0.112", "record": [{"timestamp": 35779, "value": 31, "variance": 0.0}, {}, {}] },
    #      "9": {"ip":"192.168.0.117", "record": [{"timestamp": 35787, "value": 27, "variance": 0.1}, {}, {}] },
    #   ]

    def __init__(self, reportPath):

        self.lock = Lock()
        self.reportDict = {}
        with open(reportPath, 'r') as fileObject:

            lines = fileObject.readlines()
            for line in lines:
                lineArray = line.split()

                #{date}\t{levelId}\t{ip}\t{value}\t{variance}
                dateString = lineArray[0]
#
                dateTime = parser.parse(dateString).astimezone()

                timeStamp = dateTime.timestamp() #datetime.fromtimestamp(value)
                levelId = lineArray[1]
                ip = lineArray[2]
                value = float(lineArray[3])
                variance = float(lineArray[4])

                if not levelId in self.reportDict:
                    self.reportDict[levelId] = {'ip': ip, 'record': []}

                self.reportDict[levelId]['record'].append({'timeStamp': timeStamp, 'value': value, 'variance': variance})

    def getRawReportCopy(self):
        with self.lock:
            return deepcopy(self.reportDict)

    def addRecord(self, dateString, levelId, ip, value, variance):

        with self.lock:
            dateTime = parser.parse(dateString).astimezone()

            timeStamp = dateTime.timestamp()
            if not levelId in self.reportDict:

#                logging.debug("")
#                logging.debug("")
#                logging.debug("type {0}".format(type(levelId)))
#                logging.debug("$$$ new dict key created: '{0}'".format(levelId))
#                logging.debug(self.reportDict)
#                logging.debug("")
#                logging.debug("")

                self.reportDict[levelId] = {'ip': ip, 'record': []}


#                logging.debug("")
#                logging.debug("--- new dict --- ")
#                logging.debug(self.reportDict)
#                logging.debug("")
#                logging.debug("")
#                logging.debug("")
#                logging.debug("")

            self.reportDict[levelId]['record'].append({'timeStamp': timeStamp, 'value': value, 'variance': variance})


#            logging.debug( "$$$ {0} added to the reportDict ({1})  - $$$}".format(timeStamp, value) )
#            logging.debug( "$$$ {0} added to the reportDict ({1}) $$$".format(timeStamp,value ))



    def filterReportCopy(self, reportCopy, startDateStamp, endDateStamp=None):
        """
        return reportCopy
        [
              "5": {"ip":"192.168.0.112", "record": [{"timeStamp": 35779, "value": 31, "variance": 0.0}, {}, {}] },
              "9": {"ip":"192.168.0.117", "record": [{"timeStamp": 35787, "value": 27, "variance": 0.1}, {}, {}] },
        ]
        """
        # if NO endDateStamp provided
        if endDateStamp == None:

            # takes NOW as endDateStamp
            endDateStamp = datetime.now().astimezone().timestamp()

        for levelId in reportCopy:

            for c in list(reportCopy[levelId]["record"]):
                if c['timeStamp'] < startDateStamp or c['timeStamp'] > endDateStamp:
                    reportCopy[levelId]['record'].remove(c)

        return reportCopy

    def smoothReportCopy(self, reportCopy, window=15):
        """
        return reportCopy
        [
              "5": {"ip":"192.168.0.112", "record": [{"timeStamp": 35779, "value": 31, "variance": 0.0}, {}, {}] },
              "9": {"ip":"192.168.0.117", "record": [{"timeStamp": 35787, "value": 27, "variance": 0.1}, {}, {}] },
        ]
        """
        for levelId in reportCopy:
            timeStamps = [r['timeStamp'] for r in reportCopy[levelId]["record"]]

            # collect levels
            values = [r['value'] for r in reportCopy[levelId]["record"]]

            # smooth curve
            newValues = self.smooth(values, min(window, len(values)))

            for r, v in zip( reportCopy[levelId]["record"], newValues):
                r.update({'value': v})

            reportCopy[levelId]['record'] = reportCopy[levelId]['record'][window:]

        print()
        print(reportCopy)
        print("----")

        return reportCopy



    def calculateTrendForReportCopy(self, reportCopy):
        """
        return reportCopy
            {
              "5": {"ip":"192.168.0.112", "slope": -1.2, "intercept": 0.234, 'stdError': 0.002, "record": [{"timestamp": 35779, "date": "2021-11-12T21:12:22.12345+01:00", "value": 31, "variance": 0.0}, {}, {}] },
              "9": {"ip":"192.168.0.117", "slope": 0.72, "intercept": 123.7, 'stdError': 0.021, "record": [{"timestamp": 35787, "date": "2021-11-12T21:12:25.34512+01:00", "value": 27, "variance": 0.1}, {}, {}] },
            }
        """
        for levelId in reportCopy:

            ip = reportCopy[levelId]['ip']

            dataCollection = {'x': [], 'y': []}   # for trend

            for record in reportCopy[levelId]['record']:
                timeStamp = record['timeStamp']

                value = float(record['value'])
                variance = float(record['variance'])

#                logging.debug( "recordValue: {0}, value: {1}".format(record['value'], value) )

                dataCollection['x'].append(timeStamp)  # for trend
                dataCollection['y'].append(value)      # for trend

#            logging.debug( "SIZE of dataCollection: {0}".format(len(dataCollection['x'])) )

            # for trend
#            if len(dataCollection['x']) > 10:
            std_err = 0
            if len(dataCollection['x']) > 1:

                slope, intercept = self.getRegression(dataCollection['x'], dataCollection['y'])
#                slope, intercept, r, p, std_err = stats.linregress(dataCollection['x'], dataCollection['y'])
            else:
                slope = None
                intercept = None
#                std_err = None

#            logging.debug( "TREND PAR - slope: {0}, intercept: {1}".format(slope, intercept) )


#            logging.debug( "DATACOLLECTION[X]: {0}".format(dataCollection['x']) )
#            logging.debug( "DATACOLLECTION[Y]: {0}".format(dataCollection['y']) )


            reportCopy[levelId]['slope'] = slope
            reportCopy[levelId]['intercept'] = intercept
#            reportCopy[levelId]['stdError'] = std_err

        return reportCopy

    def getGraphFromReportCopy(self, reportCopy, levelId=None):
        retDict = {}

        for actualLevelId in reportCopy:

            if levelId and levelId != actualLevelId:
                continue

            #levelDict = reportCopy[levelId]
            #ip = levelDict['ip']
            slope = reportCopy[actualLevelId]['slope']
            intercept = reportCopy[actualLevelId]['intercept']
            #stdError = levelDict['stdError']
            recordList = reportCopy[actualLevelId]['record']

            # Input
            measure_timestamps = [record['timeStamp'] for record in recordList]
            measure_dates = [datetime.fromtimestamp(ts) for ts in measure_timestamps]
            measure_values = [record['value'] for record in recordList]

            if len(measure_dates) > 1:
                trend_dates = [measure_dates[0], measure_dates[-1]]
                trend_values = [measure_timestamps[0] * slope + intercept, measure_timestamps[-1] * slope + intercept]
            else:
                trend_dates = []
                trend_values = []
#            logging.debug( "TREND - {0}: {1}, {2}, {3}".format(trend_dates[0], trend_values[0], trend_dates[1], trend_values[1]) )

            # clean plt
            plt.clf()

            plt.rcParams.update({'figure.autolayout': True})
            plt.tight_layout()
            #plt.subplots_adjust(bottom=0.30)
            px = 1/plt.rcParams['figure.dpi'] # pixel in inches
#            plt.subplots(figsize=(1200*px, 600*px))
            plt.xticks(rotation=25)

            ax=plt.gca()

            # configure tick locators
            x_major_locator=md.DayLocator()
            x_minor_locator=md.HourLocator(interval=1)
            ax.xaxis.set_major_locator(x_major_locator)
            ax.xaxis.set_minor_locator(x_minor_locator)

            # format X values
            #xfmt=md.DateFormatter('%Y-%m-%d %H:%M:%S')
            xfmt=md.DateFormatter('%Y-%m-%d %H:%M')
            ax.xaxis.set_major_formatter(xfmt)

            ax.set(xlabel="time", ylabel='level [mm]', title=f'Sensor {actualLevelId}')
            ax.grid()

            plt.plot(measure_dates, measure_values, label="Measure", linewidth='1', color='green')
            plt.plot(trend_dates, trend_values, label="Trend", linewidth='3', color='red')

            plt.legend()

            fileName = f'graph_{actualLevelId}.jpg'

            retDict[actualLevelId] = fileName

            logging.debug( "!!! Start saving" )

            plt.savefig(fileName)

            logging.debug( "!!! End saving." )

        return retDict

    def getGraphs(self, startDateStamp, endDateStamp=None, window=15):

#        logging.debug( "!!! - start copy !!!" )
        reportCopy = self.getRawReportCopy()
#        logging.debug( "!!! - end copy. length: {0}!!!".format(len(reportCopy['6']['record']) ) )

#        logging.debug( "!!! - start filter !!!" )
        self.filterReportCopy(reportCopy, startDateStamp)
#        logging.debug( "!!! - end filter !!!" )

#        logging.debug( "!!! - start smoothing !!!" )
        self.smoothReportCopy(reportCopy, window=window)
#        logging.debug( "!!! - end smoothing !!!" )

#        logging.debug( "!!! - start trend !!!" )
        self.calculateTrendForReportCopy(reportCopy)
#        logging.debug( "!!! - end trend. length: {0}!!!".format(len(reportCopy['6']['record']) ) )

        logging.debug( "!!! - start graph !!!" )
        ret = self.getGraphFromReportCopy(reportCopy, levelId=None)
        logging.debug( "!!! - end graph !!!" )

        return ret


    def smooth(self, y, winsize=5):
        return np.array(pd.Series(y).rolling(winsize).mean())

    def getVariance(self, arr, mean):
        return np.sum((arr-mean)**2)

    def getCovariance(self, arr_x, mean_x, arr_y, mean_y):
        final_arr = (arr_x-mean_x)*(arr_y-mean_y)
        return np.sum(final_arr)

    def getRegression(self, x, y):

        x_mean = np.mean(x)
        y_mean = np.mean(y)

        m = self.getCovariance(x, x_mean, y, y_mean)/self.getVariance(x, x_mean)
        b = y_mean - x_mean*m

        return m, b