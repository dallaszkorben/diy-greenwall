import logging
from exceptions.invalid_api_usage import InvalidAPIUsage
from webserver.endpoints.ep import EP
import datetime
from flask import request
from webserver.representations import output_json
from dateutil import parser
import numpy as np
#from sklearn.linear_model import LinearRegression
#import pandas as pd


class EPInfoTrend(EP):

    ID = 'info_trend'
    URL = '/info/trend'

    PATH_PAR_PAYLOAD = '/trend'
    PATH_PAR_URL = '/trend/startDate/<startDate>'

    METHOD = 'GET'

    ATTR_START_DATE = 'startDate'

    def __init__(self, web_gadget):
        self.web_gadget = web_gadget

    @staticmethod
    def getRequestDescriptionWithPayloadParameters():

        ret = {}
        ret['id'] = EPInfoTrend.ID
        ret['method'] = EPInfoTrend.METHOD
        ret['path-parameter-in-payload'] = EPInfoTrend.PATH_PAR_PAYLOAD
        ret['path-parameter-in-url'] = EPInfoTrend.PATH_PAR_URL

        ret['parameters'] = [{}]

        ret['parameters'][0]['attribute'] = EPInfoTrend.ATTR_START_DATE
        ret['parameters'][0]['type'] = 'string'
        ret['parameters'][0]['min'] = datetime.datetime(2000, 1,1).astimezone().isoformat()
        ret['parameters'][0]['max'] = datetime.datetime.now().astimezone().isoformat()

        return ret

    def executeByParameters(self, startDate) -> dict:
        payload = {}
        payload[EPInfoTrend.ATTR_START_DATE] = startDate
        return self.executeByPayload(payload)

    def executeByPayload(self, payload) -> dict:
        parameterStartDateString = payload[EPInfoTrend.ATTR_START_DATE]
        startDateString = parser.parse(parameterStartDateString).astimezone().isoformat()
        startDate = parser.parse(startDateString)

        logging.debug( "WEB request: {0} {1} ('{2}': {3})".format(
                    EPInfoTrend.METHOD, EPInfoTrend.URL,
                    EPInfoTrend.ATTR_START_DATE, startDateString
                    )
            )

        ret = {'result': 'OK', 'trend': {}}
        rawList = {}
        with open(self.web_gadget.reportPath, 'r') as fileObject:

            lines = fileObject.readlines()
            for line in lines:
                lineArray = line.split()

                #{date}\t{levelId}\t{ip}\t{value}\t{variance}
                dateString = lineArray[0]
                date = parser.parse(dateString)
                if date >= startDate:
                    levelId = lineArray[1]
                    #ip = lineArray[2]
                    value = int(lineArray[3])
                    #variance = float(lineArray[4])

                    if not levelId in rawList:
                        rawList[levelId] = {'x': [], 'y': []}
                    rawList[levelId]['x'].append(date.timestamp()) #datetime.fromtimestamp(value)
                    rawList[levelId]['y'].append(value)


        return output_json( {}, EP.CODE_OK)
#        return output_json( rawList, EP.CODE_OK)
