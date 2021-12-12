import logging
from exceptions.invalid_api_usage import InvalidAPIUsage
from restserver.endpoints.ep import EP
from flask import request
from restserver.representations import output_json

from graph.graph_level import GraphLevel

from dateutil import parser
from datetime import datetime

import numpy as np

#from sklearn.linear_model import LinearRegression
#import pandas as pd
from scipy import stats

class EPInfoGraph(EP):

    ID = 'info_graph'
    URL = '/info/graph'

    PATH_PAR_PAYLOAD = '/graph'
    PATH_PAR_URL = '/graph/startDate/<startDate>'
#    PATH_PAR_URL = '/graph/startDate/<startDate>/sensorId/<sensorId>'

    METHOD = 'GET'

    ATTR_START_DATE = 'startDate'
#    ATTR_SENSOR_ID = 'sensorId'

    def __init__(self, web_gadget):
        self.web_gadget = web_gadget

    @staticmethod
    def getRequestDescriptionWithPayloadParameters():

        ret = {}
        ret['id'] = EPInfoGraph.ID
        ret['method'] = EPInfoGraph.METHOD
        ret['path-parameter-in-payload'] = EPInfoGraph.PATH_PAR_PAYLOAD
        ret['path-parameter-in-url'] = EPInfoGraph.PATH_PAR_URL

        ret['parameters'] = [{}]

        ret['parameters'][0]['attribute'] = EPInfoGraph.ATTR_START_DATE
        ret['parameters'][0]['type'] = 'date'
        ret['parameters'][0]['min'] = datetime.datetime(2000, 1,1).astimezone().isoformat()
        ret['parameters'][0]['max'] = datetime.datetime.now().astimezone().isoformat()

#        ret['parameters'][1]['attribute'] = EPInfoGraph.ATTR_SENSOR_ID
#        ret['parameters'][1]['type'] = 'string'

        return ret

#    def executeByParameters(self, startDate, sensorId) -> dict:
    def executeByParameters(self, startDate) -> dict:
        payload = {}
        payload[EPInfoGraph.ATTR_START_DATE] = startDate
#        payload[EPInfoGraph.ATTR_SENSOR_ID] = sensorId
        return self.executeByPayload(payload)

    def executeByPayload(self, payload) -> dict:
        parameterStartDateString = payload[EPInfoGraph.ATTR_START_DATE]
#        parameterSensorIdString = payload[EPInfoGraph.ATTR_SENSOR_ID]

        startDateString = parser.parse(parameterStartDateString).astimezone().isoformat()
        startDateTime = parser.parse(startDateString)
        startDateStamp = datetime.timestamp(startDateTime)

#        logging.debug( "WEB request: {0} {1} ('{2}': {3}, '{4}': {5} )".format(
#                    EPInfoGraph.METHOD, EPInfoGraph.URL,
#                    EPInfoGraph.ATTR_START_DATE, startDateString,
#                    EPInfoGraph.ATTR_SENSOR_ID, parameterSensorIdString
#                    )
#        )

        logging.debug( "WEB request: {0} {1} ('{2}': {3} )".format(
                    EPInfoGraph.METHOD, EPInfoGraph.URL,
                    EPInfoGraph.ATTR_START_DATE, startDateString
                )
        )

#        graphs = self.web_gadget.report.getImageOfGrapWithTrend(startDateStamp, endDateStamp=None, sensorId=parameterSensorIdString)
        reportCopy = self.web_gadget.report.getRawReportCopy()
        webFolderName = self.web_gadget.webFolderName
        webPathNameGraph = self.web_gadget.webPathNameGraph
        webSmoothingWindow = self.web_gadget.webSmoothingWindow
        graphs = GraphLevel.getGraphs(reportCopy, startDateStamp, endDateStamp=None, window=webSmoothingWindow, webFolderName=webFolderName, webPathNameGraph=webPathNameGraph)
#        graphs = GraphLevel.getGraphs(startDateStamp, endDateStamp=None, window=16, webFolderName=webFolderName, webPathNameGraph=webPathNameGraph)

        ret = {'result': 'OK', 'graphs': graphs}
        return output_json( ret, EP.CODE_OK)

