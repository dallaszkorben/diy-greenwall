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

class GraphLevel:

    @staticmethod
    def filterReportCopy(reportCopy, startDateStamp, endDateStamp=None):
        """
        return reportCopy
        [
              "5": {"ip":"192.168.0.112", "record": [{"timeStamp": 35779, "levelValue": 31, "levelVariance": 0.0, "temperatureValue": 19.3, "humidityValue": 20}, {}, {}] },
              "9": {"ip":"192.168.0.117", "record": [{"timeStamp": 35787, "levelValue": 27, "levelVariance": 0.1, "temperatureValue": None, "humidityValue": None}, {}, {}] },
        ]
        """
        # if NO endDateStamp provided
        if endDateStamp == None:

            # takes NOW as endDateStamp
            endDateStamp = datetime.now().astimezone().timestamp()

        for stationId in reportCopy:

            for c in list(reportCopy[stationId]["record"]):
                if c['timeStamp'] < startDateStamp or c['timeStamp'] > endDateStamp:
                    reportCopy[stationId]['record'].remove(c)

        return reportCopy

    @staticmethod
    def smoothReportCopy(reportCopy, window=15):
        """
        return reportCopy
        [
              "5": {"ip":"192.168.0.112", "record": [{"timeStamp": 35779, "levelValue": 31, "levelVariance": 0.0, "temperatureValue": 19.3, "humidityValue": 20}, {}, {}] },
              "9": {"ip":"192.168.0.117", "record": [{"timeStamp": 35787, "levelValue": 27, "levelVariance": 0.1, "temperatureValue": None, "humidityValue": None}, {}, {}] },
        ]
        """

        for stationId in reportCopy:
            timeStamps = [r['timeStamp'] for r in reportCopy[stationId]["record"]]

            # collect levels
            values = [r['levelValue'] for r in reportCopy[stationId]["record"]]

            # smooth curve
            newValues = GraphLevel.smooth(values, min(window, len(values)))

            for r, v in zip( reportCopy[stationId]["record"], newValues):
                r.update({'levelValue': v})

            reportCopy[stationId]['record'] = reportCopy[stationId]['record'][window:]

        return reportCopy


    @staticmethod
    def calculateTrendForReportCopy(reportCopy):
        """
        return reportCopy
            {
              "5": {"ip":"192.168.0.112", "slope": -1.2, "intercept": 0.234, 'stdError': 0.002, "record": [{"timestamp": 35779, "date": "2021-11-12T21:12:22.12345+01:00", "levelValue": 31, "levelVariance": 0.0, "temperatureValue": 19.3, "humidityValue": 2}, {}, {}] },
              "9": {"ip":"192.168.0.117", "slope": 0.72, "intercept": 123.7, 'stdError': 0.021, "record": [{"timestamp": 35787, "date": "2021-11-12T21:12:25.34512+01:00", "levelValue": 31, "levelVariance": 0.0, "temperatureValue": None, "humidityValue": None}, {}, {}] },
            }
        """
        for stationId in reportCopy:

            ip = reportCopy[stationId]['ip']

            dataCollection = {'x': [], 'y': []}   # for trend

            for record in reportCopy[stationId]['record']:
                timeStamp = record['timeStamp']

                value = float(record['levelValue'])
                variance = float(record['levelVariance'])

                dataCollection['x'].append(timeStamp)  # for trend
                dataCollection['y'].append(value)      # for trend

            # for trend
            if len(dataCollection['x']) > 1:

                slope, intercept = GraphLevel.getRegression(dataCollection['x'], dataCollection['y'])
            else:
                slope = None
                intercept = None

            reportCopy[stationId]['slope'] = slope
            reportCopy[stationId]['intercept'] = intercept

        return reportCopy

    @staticmethod
    def getGraphFromReportCopy(reportCopy, stationId=None, webFolderName="."):
        retDict = {}

        for actualStationId in reportCopy:

            if len(reportCopy[actualStationId]['record']) == 0:
                continue

            if stationId and stationId != actualStationId:
                continue

#            print(reportCopy[actualLevelId])

            slope = reportCopy[actualStationId]['slope']
            intercept = reportCopy[actualStationId]['intercept']

            recordList = reportCopy[actualStationId]['record']
            speedInmmPerDay = slope * 86400 # 60*60*24 => mm/day
            speedInmmPerDayString = "{0:.1f} [mm/day]".format(speedInmmPerDay)

            # Input
            measure_timestamps = [record['timeStamp'] for record in recordList]
            measure_dates = [datetime.fromtimestamp(ts) for ts in measure_timestamps]
            measure_values = [record['levelValue'] for record in recordList]

            if len(measure_dates) > 1:
                trend_dates = [measure_dates[0], measure_dates[-1]]
                trend_values = [measure_timestamps[0] * slope + intercept, measure_timestamps[-1] * slope + intercept]
            else:
                trend_dates = []
                trend_values = []

            # clean plt
            plt.clf()

            plt.rcParams.update({'figure.autolayout': True})
            plt.tight_layout()
            #plt.subplots_adjust(bottom=0.30)

#            px = 1/plt.rcParams['figure.dpi'] # pixel in inches
#            plt.subplots(figsize=(1200*px, 600*px))
            plt.xticks(rotation=25)

            plt.text(measure_dates[0], measure_timestamps[0] * slope + intercept, speedInmmPerDayString)

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

            ax.set(xlabel="time", ylabel='level [mm]', title=f'Sensor {actualStationId}')
            ax.grid()

            plt.plot(measure_dates, measure_values, label="Measure", linewidth='1', color='green')
            plt.plot(trend_dates, trend_values, label="Trend", linewidth='3', color='red')

            plt.legend()

            fileName = f'{webFolderName}/graph-images/graph_level_{actualStationId}.jpg'

            retDict[actualStationId] = {'level': None, 'temperature': None, 'humidity': None}
            retDict[actualStationId]['level'] = fileName

            plt.savefig(fileName)
#            plt.savefig("../web-client/graphs/" + fileName)
#            plt.savefig(fileName)


        return retDict

    @staticmethod
    def getGraphs(reportCopy, startDateStamp, endDateStamp=None, window=15, webFolderName="."):

        #reportCopy = self.getRawReportCopy()
        GraphLevel.smoothReportCopy(reportCopy, window=window)
        GraphLevel.calculateTrendForReportCopy(reportCopy)
        ret = GraphLevel.getGraphFromReportCopy(reportCopy, stationId=None, webFolderName=webFolderName)

        return ret

    @staticmethod
    def smooth(y, winsize=5):
        return np.array(pd.Series(y).rolling(winsize).mean())

    @staticmethod
    def getVariance(arr, mean):
        return np.sum((arr-mean)**2)

    @staticmethod
    def getCovariance(arr_x, mean_x, arr_y, mean_y):
        final_arr = (arr_x-mean_x)*(arr_y-mean_y)
        return np.sum(final_arr)

    @staticmethod
    def getRegression(x, y):

        x_mean = np.mean(x)
        y_mean = np.mean(y)

        m = GraphLevel.getCovariance(x, x_mean, y, y_mean)/GraphLevel.getVariance(x, x_mean)
        b = y_mean - x_mean*m

        return m, b