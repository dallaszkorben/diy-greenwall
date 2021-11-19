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

                logging.debug("")
                logging.debug("")
                logging.debug("type {0}".format(type(levelId)))
                logging.debug("$$$ new dict key created: '{0}'".format(levelId))
                logging.debug(self.reportDict)
                logging.debug("")
                logging.debug("")

                self.reportDict[levelId] = {'ip': ip, 'record': []}


                logging.debug("")
                logging.debug("--- new dict --- ")
                logging.debug(self.reportDict)
                logging.debug("")
                logging.debug("")
                logging.debug("")
                logging.debug("")

            self.reportDict[levelId]['record'].append({'timeStamp': timeStamp, 'value': value, 'variance': variance})


#            logging.debug( "$$$ {0} added to the reportDict ({1})  - $$$}".format(timeStamp, value) )
            logging.debug( "$$$ {0} added to the reportDict ({1}) $$$".format(timeStamp,value ))



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

                dataCollection['x'].append(timeStamp)  # for trend
                dataCollection['y'].append(value)      # for trend

                # for trend
                if len(dataCollection['x']) > 10:
                    slope, intercept, r, p, std_err = stats.linregress(dataCollection['x'], dataCollection['y'])

                else:
                    slope = None
                    intercept = None
                    std_err = None

            reportCopy[levelId]['slope'] = slope
            reportCopy[levelId]['intercept'] = intercept
            reportCopy[levelId]['stdError'] = std_err

            return reportCopy

    def getGraphFromReportCopy(self, reportCopy, levelId=None):
        retDict = {}

        for actualLevelId in reportCopy:

            if levelId and levelId != actualLevelId:
                continue

            #levelDict = reportCopy[levelId]
            #ip = levelDict['ip']
#            slope = levelDict['slope']
#            intercept = levelDict['intercept']
            #stdError = levelDict['stdError']
            recordList = reportCopy[actualLevelId]['record']

            # Input
            measure_timestamps = [record['timeStamp'] for record in recordList]
            measure_dates = [datetime.fromtimestamp(ts) for ts in measure_timestamps]
            measure_values = [record['value'] for record in recordList]

            # clean plt
            plt.clf()

            plt.rcParams.update({'figure.autolayout': True})
            plt.tight_layout()
            #plt.subplots_adjust(bottom=0.30)
            px = 1/plt.rcParams['figure.dpi'] # pixel in inches
            plt.subplots(figsize=(1200*px, 600*px))
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

            ax.set(xlabel="time", ylabel='level [mm]', title=f'Sensor {levelId}')
            ax.grid()

            plt.plot(measure_dates, measure_values, label="Measure", linewidth='1', color='green')
            #plt.plot(trend_dates, trend_value, label="Trend", linewidth='3', color='red')

            plt.legend()

            fileName = f'graph_{actualLevelId}.png'

            retDict[actualLevelId] = fileName

            plt.savefig(fileName)

            return retDict

    def getGraphs(self, startDateStamp, endDateStamp=None, window=15):

        logging.debug( "!!! - start copy !!!" )
        reportCopy = self.getRawReportCopy()
        logging.debug( "!!! - end copy. length: {0}!!!".format(len(reportCopy['6']['record']) ) )

        logging.debug( "!!! - start filter !!!" )
        self.filterReportCopy(reportCopy, startDateStamp)
        logging.debug( "!!! - end filter !!!" )

        logging.debug( "!!! - start smoothing !!!" )
        self.smoothReportCopy(reportCopy, window=window)
        logging.debug( "!!! - end smoothing !!!" )

        logging.debug( "!!! - start trend !!!" )
        self.calculateTrendForReportCopy(reportCopy)
        logging.debug( "!!! - end trend. length: {0}!!!".format(len(reportCopy['6']['record']) ) )

        logging.debug( "!!! - start graph !!!" )
        ret = self.getGraphFromReportCopy(reportCopy, levelId=None)
        logging.debug( "!!! - end graph !!!" )

        return ret







































    def getFilteredLevels(self, startDateStamp=None, endDateStamp=None, sensorId=None):
        """
        return
        [
              "5": {"ip":"192.168.0.112", "record": [{"timeStamp": 35779, "value": 31, "variance": 0.0}, {}, {}] },
              "9": {"ip":"192.168.0.117", "record": [{"timeStamp": 35787, "value": 27, "variance": 0.1}, {}, {}] },
        ]
        """
        with self.lock:
            retDict = {}
            if endDateStamp == None:
                endDateStamp = datetime.now().astimezone().timestamp()

            for levelId in self.reportDict:

                if sensorId and sensorId != levelId:
                    continue

                ip = self.reportDict[levelId]['ip']

                newRecordList = [r for r in self.reportDict[levelId]["record"] if r['timeStamp'] >= startDateStamp and r['timeStamp'] <= endDateStamp]
                retDict[levelId] = {'ip': ip, 'record': newRecordList}

            return retDict


    def getFilteredLevelWithTrend(self, startDateStamp=None, endDateStamp=None, sensorId=None):
        """
        return:
            {
              "5": {"ip":"192.168.0.112", "slope": -1.2, "intercept": 0.234, 'stdError': 0.002, "record": [{"timestamp": 35779, "date": "2021-11-12T21:12:22.12345+01:00", "value": 31, "variance": 0.0}, {}, {}] },
              "9": {"ip":"192.168.0.117", "slope": 0.72, "intercept": 123.7, 'stdError': 0.021, "record": [{"timestamp": 35787, "date": "2021-11-12T21:12:25.34512+01:00", "value": 27, "variance": 0.1}, {}, {}] },
            }
        """

#        with self.lock:
        if True:

            retDict = {}
            if endDateStamp == None:
                endDateStamp = datetime.now().astimezone().timestamp()

            for levelId in self.reportDict:

                ip = self.reportDict[levelId]['ip']

                retRecordList = []
                dataCollection = {'x': [], 'y': []}   # for trend

                if sensorId and sensorId != levelId:
                    continue

                for record in self.reportDict[levelId]['record']:
                    timeStamp = record['timeStamp']

                    if timeStamp >= startDateStamp and timeStamp <= endDateStamp:
                        dateString = datetime.fromtimestamp(timeStamp).astimezone().isoformat()

                        value = int(record['value'])
                        variance = float(record['variance'])

                        retRecordList.append({'timeStamp': timeStamp, 'date': dateString, 'value': value, 'variance': variance})

                        dataCollection['x'].append(timeStamp)  # for trend
                        dataCollection['y'].append(value)      # for trend

                # for trend
                if len(dataCollection['x']) > 10:
                    slope, intercept, r, p, std_err = stats.linregress(dataCollection['x'], dataCollection['y'])

                else:
                    slope = None
                    intercept = None
                    std_err = None

                retDict[levelId] = {'ip': ip, "slope": slope, "intercept": intercept, 'stdError': std_err, 'record': retRecordList}

            return retDict

    def getImageOfGrapWithTrend(self, startDateStamp=None, endDateStamp=None, sensorId=None):

#        with self.lock:

        if True:

            retDict = {}
#        collectionDict = self.getFilteredLevelWithTrend(startDateStamp, endDateStamp, sensorId)

            print('call smoothing')

            collectionDict = self.getSmoothLevels(startDateStamp, endDateStamp, sensorId)

            print('for started')

            for levelId in collectionDict:

                print('   ', levelId)

                levelDict = collectionDict[levelId]
            #ip = levelDict['ip']
#            slope = levelDict['slope']
#            intercept = levelDict['intercept']
            #stdError = levelDict['stdError']
                recordList = levelDict['record']

                # Input
                measure_timestamps = [record['timeStamp'] for record in recordList]
                measure_dates = [datetime.fromtimestamp(ts) for ts in measure_timestamps]
                measure_values = [record['value'] for record in recordList]

                print('   graph started')

                # clean plt
                plt.clf()

                plt.rcParams.update({'figure.autolayout': True})
                plt.tight_layout()
                #plt.subplots_adjust(bottom=0.30)
                px = 1/plt.rcParams['figure.dpi'] # pixel in inches
                plt.subplots(figsize=(1200*px, 600*px))
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

                ax.set(xlabel="time", ylabel='level [mm]', title=f'Sensor {levelId}')
                ax.grid()

                plt.plot(measure_dates, measure_values, label="Measure", linewidth='1', color='green')
                #plt.plot(trend_dates, trend_value, label="Trend", linewidth='3', color='red')

                plt.legend()

                fileName = f'graph_{levelId}.png'

                retDict[levelId] = fileName

                print('   start to save')

                plt.savefig(fileName)

            return retDict

    def getSmoothLevels(self, startDateStamp=None, endDateStamp=None, sensorId=None):
        """
        return
        [
              "5": {"ip":"192.168.0.112", "record": [{"timeStamp": 35779, "value": 31, "variance": 0.0}, {}, {}] },
              "9": {"ip":"192.168.0.117", "record": [{"timeStamp": 35787, "value": 27, "variance": 0.1}, {}, {}] },
        ]
        """
#        with self.lock:
        if True:

            print('      smothing started')

            filteredLevelDict = self.getFilteredLevels(startDateStamp, endDateStamp, sensorId)

            for levelId in filteredLevelDict:
                timeStamps = [r['timeStamp'] for r in filteredLevelDict[levelId]["record"]]
                values = [r['value'] for r in filteredLevelDict[levelId]["record"]]

                #smooth curve
                newValues = self.smooth(values, min(30, len(values)))

                [ r.update({'value': v}) for r, v in zip( filteredLevelDict[levelId]["record"], newValues) ]

            return filteredLevelDict

    def smooth1(self, y, box_pts):
        box=np.ones(box_pts)/box_pts
        y_smooth=np.convolve(y, box, mode='same')
        return y_smooth

    def smooth(self, y, winsize=5):
        return np.array(pd.Series(y).rolling(winsize).mean())
