import logging
from exceptions.invalid_api_usage import InvalidAPIUsage
from webserver.endpoints.ep import EP
import datetime
from flask import request
from webserver.representations import output_json

class EPLevelAdd(EP):

    ID = 'level_add'
    URL = '/level/add'

    PATH_PAR_PAYLOAD = '/add'
    PATH_PAR_URL = '/add/levelId/<levelId>/value/<value>/variance/<variance>'

    METHOD = 'POST'

    ATTR_LEVEL_ID = 'levelId'
    ATTR_VALUE = 'value'
    ATTR_VARIANCE = 'variance'

    def __init__(self, web_gadget):
        self.web_gadget = web_gadget

    @staticmethod
    def getRequestDescriptionWithPayloadParameters():

        ret = {}
        ret['id'] = EPLevelAdd.ID
        ret['method'] = EPLevelAdd.METHOD
        ret['path-parameter-in-payload'] = EPLevelAdd.PATH_PAR_PAYLOAD
        ret['path-parameter-in-url'] = EPLevelAdd.PATH_PAR_URL

        ret['parameters'] = [{},{},{}]

        ret['parameters'][0]['attribute'] = EPLevelAdd.ATTR_LEVEL_ID
        ret['parameters'][0]['type'] = 'string'
        ret['parameters'][0]['value'] = 1

        ret['parameters'][1]['attribute'] = EPLevelAdd.ATTR_VALUE
        ret['parameters'][1]['type'] = 'integer'
        ret['parameters'][1]['min'] = 0
        ret['parameters'][1]['max'] = 100

        ret['parameters'][2]['attribute'] = EPLevelAdd.ATTR_VARIANCE
        ret['parameters'][2]['type'] = 'decimal'
        ret['parameters'][2]['min'] = -100
        ret['parameters'][2]['max'] = 100

        return ret

    def executeByParameters(self, levelId, value, variance) -> dict:
        payload = {}
        payload[EPLevelAdd.ATTR_LEVEL_ID] = levelId
        payload[EPLevelAdd.ATTR_VALUE] = int(value)
        payload[EPLevelAdd.ATTR_VARIANCE] = float(variance)
        return self.executeByPayload(payload)


    def executeByPayload(self, payload) -> dict:

        levelId = payload[EPLevelAdd.ATTR_LEVEL_ID]
        value = int(payload[EPLevelAdd.ATTR_VALUE])
        variance = float(payload[EPLevelAdd.ATTR_VARIANCE])

        logging.debug( "WEB request: {0} {1} ('{2}': {3}, '{4}': {5}, '{6}': {7})".format(
                    EPLevelAdd.METHOD, EPLevelAdd.URL,
                    EPLevelAdd.ATTR_LEVEL_ID, levelId,
                    EPLevelAdd.ATTR_VALUE, value,
                    EPLevelAdd.ATTR_VARIANCE, variance,
                    )
            )

        date = datetime.datetime.now().astimezone().isoformat()
        ip = request.remote_addr
        #self.web_gadget.appendLevelData(date, levelId, value, variance)

        with open(self.web_gadget.reportPath, 'a') as fileObject:
            fileObject.write(f'{date}\t{levelId}\t{ip}\t{value}\t{variance}\n')

        return output_json( {'result': 'OK'}, EP.CODE_OK)

