import logging

from dateutil import parser
from datetime import datetime

from copy import deepcopy

import time

from threading import Lock

class ReportSensor:

    def __init__(self, reportPath, db):

        self.db = db


    def getLatestValues(self, stationId=None):

        output = self.db.get_latest_values(stationId)

        return output


    def addRecordSensor(self, dateString, stationId, ip, levelValue, temperatureValue, humidityValue, pressureValue):

        self.db.append_report(stationId, ip, dateString, pressure=pressureValue, humidity=humidityValue, level=levelValue, temperature=temperatureValue)