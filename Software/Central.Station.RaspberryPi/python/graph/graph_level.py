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

            reportCopy[stationId]['record'] = reportCopy[stationId]['record'][window-1:]


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
    def getGraphFromReportCopy(reportCopy, stationId=None, webFolderName=".", webPathNameGraph="graph-images"):
        retList = []

        # Go through all stations
        for actualStationId in reportCopy:

            # No record for the station (empty) - takes the next
            if len(reportCopy[actualStationId]['record']) == 0:
                continue

            # Thre is Station filter but the actual Station is not that - takes the next
            if stationId and stationId != actualStationId:
                continue

            # Prepare the response
            retDict = {'stationId': actualStationId, 'levelPath': None, 'temperaturePath': None, 'humidityPath': None}

            slope = reportCopy[actualStationId]['slope']
            intercept = reportCopy[actualStationId]['intercept']

            recordList = reportCopy[actualStationId]['record']
            speedInmmPerDay = slope * 86400 # 60*60*24 => mm/day
            speedInmmPerDayString = "{0:.1f} [mm/day]".format(speedInmmPerDay)

#            import pprint
#            print("---")
#            pprint.pprint(recordList)

            # Collect inputs
            measure_timestamps = [record['timeStamp'] for record in recordList]
            measure_dates = [datetime.fromtimestamp(ts) for ts in measure_timestamps]
            measure_level_values = [record['levelValue'] for record in recordList]
            measure_temperature_values = [record['temperatureValue'] for record in recordList]
            measure_humidity_values = [record['humidityValue'] for record in recordList]


            if len(measure_dates) > 1:
                trend_dates = [measure_dates[0], measure_dates[-1]]
                trend_values = [measure_timestamps[0] * slope + intercept, measure_timestamps[-1] * slope + intercept]
            else:
                trend_dates = []
                trend_values = []

            # -----------
            # Water Level
            # -----------

            # clean plt
            plt.clf()

            plt.rcParams.update({'figure.autolayout': True})
            plt.xticks(rotation=25)
            plt.text(measure_dates[0], measure_timestamps[0] * slope + intercept, speedInmmPerDayString)

            # Set range
            plt.ylim(0,110)

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

            ax.set(xlabel="", ylabel='level [mm]', title=f'Water level on Sensor {actualStationId}')
            ax.grid()

            plt.plot(measure_dates, measure_level_values, label="Measure", linewidth='1', color='green')
            plt.plot(trend_dates, trend_values, label="Trend", linewidth='3', color='red')

            plt.legend()

            fileName = f'{webFolderName}/{webPathNameGraph}/graph_level_{actualStationId}.jpg'
            pathName = f'{webPathNameGraph}/graph_level_{actualStationId}.jpg'

            retDict['levelPath'] = pathName
#            retList.append(retDict)

            plt.savefig(fileName, bbox_inches="tight")

            # -----------
            # Temperature
            # -----------

            # clean plt
            plt.clf()

#            plt.rcParams.update({'figure.autolayout': True})
            plt.xticks(rotation=25)
#            plt.text(measure_dates[0], measure_timestamps[0] * slope + intercept, speedInmmPerDayString)
            # Set range
            plt.ylim(0,40)


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

            ax.set(xlabel="", ylabel='temp [°C]', title=f'Temperature on Sensor {actualStationId}')
            ax.grid()

            plt.plot(measure_dates, measure_temperature_values, label="Measure", linewidth='1', color='blue')

#            plt.legend()

            fileName = f'{webFolderName}/{webPathNameGraph}/graph_temperature_{actualStationId}.jpg'
            pathName = f'{webPathNameGraph}/graph_temperature_{actualStationId}.jpg'

            retDict['temperaturePath'] = pathName
            retList.append(retDict)

            plt.savefig(fileName, bbox_inches="tight")

        return retList

    @staticmethod
    def getGraphs(reportCopy, startDateStamp, endDateStamp=None, window=15, webFolderName=".", webPathNameGraph="graph-images"):



        #reportCopy = self.getRawReportCopy()
        GraphLevel.smoothReportCopy(reportCopy, window=window)
        GraphLevel.calculateTrendForReportCopy(reportCopy)
        ret = GraphLevel.getGraphFromReportCopy(reportCopy, stationId=None, webFolderName=webFolderName, webPathNameGraph=webPathNameGraph)

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
        v = GraphLevel.getVariance(x, x_mean)

        if v == 0:
            m = 0
        else:
            m = GraphLevel.getCovariance(x, x_mean, y, y_mean)/v

        b = y_mean - x_mean*m

        return m, b