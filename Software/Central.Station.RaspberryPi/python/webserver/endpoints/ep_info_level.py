import logging
from exceptions.invalid_api_usage import InvalidAPIUsage
from webserver.endpoints.ep import EP
import datetime
from flask import request
from webserver.representations import output_json
from dateutil import parser

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
        startDate = parser.parse(startDateString)

        logging.debug( "WEB request: {0} {1} ('{2}': {3})".format(
                    EPInfoLevel.METHOD, EPInfoLevel.URL,
                    EPInfoLevel.ATTR_START_DATE, startDateString
                    )
            )

        ret = {'result': 'OK', 'list': []}
        with open(self.web_gadget.reportPath, 'r') as fileObject:

            lines = fileObject.readlines()
            for line in lines:
                lineArray = line.split()

                #{date}\t{levelId}\t{ip}\t{value}\t{variance}
                dateString = lineArray[0]
                date = parser.parse(dateString)
                if date >= startDate:
                    levelId = lineArray[1]
                    ip = lineArray[2]
                    value = int(lineArray[3])
                    variance = float(lineArray[4])
                    ret['list'].append({'date': dateString, 'levelId': levelId, 'ip': ip, 'value': value, 'variance': variance})

        return output_json( ret, EP.CODE_OK)
