import logging
from exceptions.invalid_api_usage import InvalidAPIUsage
from restserver.endpoints.ep import EP
from restserver.representations import output_json

from flask import request

from dateutil import parser
from datetime import datetime

class EPLampRegister(EP):

    ID = 'lamp_register'
    URL = '/lamp/register'

    PATH_PAR_PAYLOAD = '/register'
    PATH_PAR_URL = '/register/dateString/<dateString>/lampId/<lampId>'

    METHOD = 'POST'

    ATTR_LAMP_ID = 'lampId'
    ATTR_IP = 'ip'
    ATTR_DATE_STRING = 'dateString'

    def __init__(self, web_gadget):
        self.web_gadget = web_gadget

    @staticmethod
    def getRequestDescriptionWithPayloadParameters():

        ret = {}
        ret['id'] = EPLampRegister.ID
        ret['method'] = EPLampRegister.METHOD
        ret['path-parameter-in-payload'] = EPLampRegister.PATH_PAR_PAYLOAD
        ret['path-parameter-in-url'] = EPLampRegister.PATH_PAR_URL

        ret['parameters'] = [{},{},{}]

        ret['parameters'][0]['attribute'] = EPLampRegister.ATTR_LAMP_ID
        ret['parameters'][0]['type'] = 'string'
        ret['parameters'][0]['value'] = 255

        ret['parameters'][1]['attribute'] = EPLampRegister.ATTR_IP
        ret['parameters'][1]['type'] = 'string'
        ret['parameters'][1]['value'] = 255

        ret['parameters'][2]['attribute'] = EPLampRegister.ATTR_DATE_STRING
        ret['parameters'][2]['type'] = 'string'
        ret['parameters'][2]['value'] = 255

        return ret

    def executeByParameters(self, dateString, lampId) -> dict:
        payload = {}
        payload[EPLampRegister.ATTR_LAMP_ID] = lampId
        payload[EPLampRegister.ATTR_DATE_STRING] = dateString

        return self.executeByPayload(payload)

    def executeByPayload(self, payload) -> dict:

        lampId = payload[EPLampRegister.ATTR_LAMP_ID]
        dateString = payload[EPLampRegister.ATTR_DATE_STRING]

        logging.debug( "WEB request: {0} {1} ('{2}': {3}, '{4}': {5} )".format(
                    EPLampRegister.METHOD, EPLampRegister.URL,
                    EPLampRegister.ATTR_LAMP_ID, lampId,
                    EPLampRegister.ATTR_DATE_STRING, dateString
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

        self.web_gadget.registerLamp.register(dateString, lampId, ip)

        # print out to LCD
#        self.web_gadget.controlBox.refreshData(stationId)

        return output_json( {'result': 'OK'}, EP.CODE_OK)

