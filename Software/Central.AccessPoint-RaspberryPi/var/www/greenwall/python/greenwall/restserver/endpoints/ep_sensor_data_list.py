import logging

from greenwall.exceptions.invalid_api_usage import InvalidAPIUsage
from greenwall.restserver.endpoints.ep import EP
from greenwall.restserver.representations import output_json
from greenwall.graph.graph_level import GraphLevel

from flask import request

from dateutil import parser
from datetime import datetime

import numpy as np

from scipy import stats

class EPSensorDataList(EP):

    ID = 'sensor_data_list'
    URL = '/sensor/data/list'

    PATH_PAR_PAYLOAD = '/data/list'
    PATH_PAR_1_URL = '/data/list/startDate/<startDate>'
    PATH_PAR_2_URL = '/data/list/startDate/<startDate>/endDate/<endDate>'

    METHOD = 'GET'

    ATTR_START_DATE = 'startDate'
    ATTR_END_DATE = 'endDate'

    def __init__(self, web_gadget):
        self.web_gadget = web_gadget

    @staticmethod
    def getRequestDescriptionWithPayloadParameters():

        ret = {}
        ret['id'] = EPSensorDataList.ID
        ret['method'] = EPSensorDataList.METHOD
        ret['path-parameter-in-payload'] = EPSensorDataList.PATH_PAR_PAYLOAD
        ret['path-parameter-in-url'] = EPSensorDataList.PATH_PAR_1_URL

        ret['parameters'] = [{}]

        ret['parameters'][0]['attribute'] = EPSensorDataList.ATTR_START_DATE
        ret['parameters'][0]['type'] = 'date'
        ret['parameters'][0]['min'] = datetime.datetime(2000, 1,1).astimezone().isoformat()
        ret['parameters'][0]['max'] = datetime.datetime.now().astimezone().isoformat()

        return ret

    def executeByParameters(self, startDate, endDate = None) -> dict:
        payload = {}
        payload[EPSensorDataList.ATTR_START_DATE] = startDate

        payload[EPSensorDataList.ATTR_END_DATE] = endDate
        return self.executeByPayload(payload)

    def executeByPayload(self, payload) -> dict:
        parameterStartDateString = payload[EPSensorDataList.ATTR_START_DATE]
        parameterEndDateString = payload[EPSensorDataList.ATTR_END_DATE]

        startDateString = parser.parse(parameterStartDateString).astimezone().isoformat()
        startDateTime = parser.parse(startDateString)
        startDateStamp = datetime.timestamp(startDateTime)

        endDateStamp = None

        remoteAddress = request.remote_addr

        if parameterEndDateString:
            endDateString = parser.parse(parameterEndDateString).astimezone().isoformat()
            endDateTime = parser.parse(endDateString)
            endDateStamp = datetime.timestamp(endDateTime)

            logging.debug( "WEB request ({0}): {1} {2} ('{3}': {4}, {5}: {6} )".format(
                    remoteAddress, EPSensorDataList.METHOD, EPSensorDataList.URL,
                    EPSensorDataList.ATTR_START_DATE, startDateString,
                    EPSensorDataList.ATTR_END_DATE, endDateString
                )
            )
        else:
            logging.debug( "WEB request ({0}): {1} {2} ('{3}': {4} )".format(
                    remoteAddress, EPSensorDataList.METHOD, EPSensorDataList.URL,
                    EPSensorDataList.ATTR_START_DATE, startDateString
                )
            )

        reportCopy = GraphLevel.filterReportCopy(self.web_gadget.db, startDateStamp, endDateStamp)
        reportCopy = GraphLevel.smoothReportCopy(reportCopy, window=15)

        ret = {'result': 'OK', 'data': reportCopy}
        header = {'Access-Control-Allow-Origin': '*', 'Content-Type': 'application/json'}
        return output_json( ret, EP.CODE_OK, header)

