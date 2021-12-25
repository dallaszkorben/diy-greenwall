import logging
from exceptions.invalid_api_usage import InvalidAPIUsage
from restserver.endpoints.ep import EP
from flask import request
from restserver.representations import output_json

from dateutil import parser
from datetime import datetime

from scipy import stats

#
# Output:
# {
#     "result": "OK",
#     "levels": {
#      "5": {
#             "ip":"192.168.0.112",
#             "slope": 0.123,
#             "intercept": 1234.456,
#             "stdError": 0.345
#             "record": [
#                {
#                    "timeStamp": 35779,
#                    "date": "2021-11-12T21:12:22.12345+01:00",
#                    "value": 31,
#                    "variance": 0.0
#                },
#                {},
#                {}
#             ]
#      },
#      "9": {
#             "ip":"192.168.0.117",
#             "slope": 0.123,
#             "intercept": 1234.456,
#             "stdError": 0.345
#             "record": [
#                {
#                    "timestamp": 35787,
#                    "date": "2021-11-12T21:12:25.34512+01:00",
#                    "value": 27,
#                    "variance": 0.1
#                },
#                {}, 
#                {}
#             ]
#      }
# }

class EPInfoLevel(EP):

    ID = 'info_level'
    URL = '/info/level'

    PATH_PAR_PAYLOAD = '/level'
    PATH_PAR_URL = '/level/startDate/<startDate>'

    METHOD = 'GET'

    ATTR_START_DATE = 'startDate'

    def __init__(self, web_gadget):
        self.web_gadget = web_gadget

    @staticmethod
    def getRequestDescriptionWithPayloadParameters():

        ret = {}
        ret['id'] = EPInfoLevel.ID
        ret['method'] = EPInfoLevel.METHOD
        ret['path-parameter-in-payload'] = EPInfoLevel.PATH_PAR_PAYLOAD
        ret['path-parameter-in-url'] = EPInfoLevel.PATH_PAR_URL

        ret['parameters'] = [{}]

        ret['parameters'][0]['attribute'] = EPInfoLevel.ATTR_START_DATE
        ret['parameters'][0]['type'] = 'string'
        ret['parameters'][0]['min'] = datetime.datetime(2000, 1,1).astimezone().isoformat()
        ret['parameters'][0]['max'] = datetime.datetime.now().astimezone().isoformat()

        return ret

    def executeByParameters(self, startDate) -> dict:
        payload = {}
        payload[EPInfoLevel.ATTR_START_DATE] = startDate
        return self.executeByPayload(payload)

    def executeByPayload(self, payload) -> dict:
        parameterStartDateString = payload[EPInfoLevel.ATTR_START_DATE]
        startDateString = parser.parse(parameterStartDateString).astimezone().isoformat()
        startDateTime = parser.parse(startDateString)
        startDateStamp = datetime.timestamp(startDateTime)

        logging.debug( "WEB request: {0} {1} ('{2}': {3})".format(
                    EPInfoLevel.METHOD, EPInfoLevel.URL,
                    EPInfoLevel.ATTR_START_DATE, startDateString
                    )
            )

        reportCopy = self.web_gadget.report.getRawReportCopy()
        self.web_gadget.report.filterReportCopy(reportCopy, startDateStamp)
        #self.smoothReportCopy(reportCopy, window=window)
        #self.calculateTrendForReportCopy(reportCopy)

        #levels=self.web_gadget.report.getFilteredLevelWithTrend(startDateStamp, endDateStamp=None, sensorId=None)
        ret = {'result': 'OK', 'levels': reportCopy}

        return output_json( ret, EP.CODE_OK)
