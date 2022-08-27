import logging

from greenwall.exceptions.invalid_api_usage import InvalidAPIUsage
from greenwall.restserver.endpoints.ep import EP
from greenwall.restserver.representations import output_json

from flask import request

from dateutil import parser
from datetime import datetime

class EPPumpRegister(EP):

    ID = 'pump_register'
    URL = '/pump/register'

    PATH_PAR_PAYLOAD = '/register'
    PATH_PAR_URL = '/register/dateString/<dateString>/pumpId/<pumpId>'

    METHOD = 'POST'

    ATTR_PUMP_ID = 'pumpId'
    ATTR_IP = 'ip'
    ATTR_DATE_STRING = 'dateString'

    def __init__(self, web_gadget):
        self.web_gadget = web_gadget

    @staticmethod
    def getRequestDescriptionWithPayloadParameters():

        ret = {}
        ret['id'] = EPPumpRegister.ID
        ret['method'] = EPPumpRegister.METHOD
        ret['path-parameter-in-payload'] = EPPumpRegister.PATH_PAR_PAYLOAD
        ret['path-parameter-in-url'] = EPPumpRegister.PATH_PAR_URL

        ret['parameters'] = [{},{},{}]

        ret['parameters'][0]['attribute'] = EPPumpRegister.ATTR_PUMP_ID
        ret['parameters'][0]['type'] = 'string'
        ret['parameters'][0]['value'] = 255

        ret['parameters'][1]['attribute'] = EPPumpRegister.ATTR_IP
        ret['parameters'][1]['type'] = 'string'
        ret['parameters'][1]['value'] = 255

        ret['parameters'][2]['attribute'] = EPPumpRegister.ATTR_DATE_STRING
        ret['parameters'][2]['type'] = 'string'
        ret['parameters'][2]['value'] = 255

        return ret

    def executeByParameters(self, dateString, pumpId) -> dict:
        payload = {}
        payload[EPPumpRegister.ATTR_PUMP_ID] = pumpId
        payload[EPPumpRegister.ATTR_DATE_STRING] = dateString

        return self.executeByPayload(payload)

    def executeByPayload(self, payload) -> dict:

        pumpId = payload[EPPumpRegister.ATTR_PUMP_ID]
        dateString = payload[EPPumpRegister.ATTR_DATE_STRING]

        logging.debug( "SENSOR request: {0} {1} ('{2}': {3}, '{4}': {5} )".format(
                    EPPumpRegister.METHOD, EPPumpRegister.URL,
                    EPPumpRegister.ATTR_PUMP_ID, pumpId,
                    EPPumpRegister.ATTR_DATE_STRING, dateString
                    )
            )

        date = parser.parse(dateString)
        dateString = date.astimezone().isoformat()


# datetime now()
#  datetime.datetime.now().astimezone()
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

        ip = request.remote_addr

        self.web_gadget.registerPump.register(dateString, pumpId, ip)

        return output_json( {'result': 'OK'}, EP.CODE_OK)

