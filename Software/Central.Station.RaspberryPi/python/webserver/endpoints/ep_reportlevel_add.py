import logging
from exceptions.invalid_api_usage import InvalidAPIUsage
from webserver.endpoints.ep import EP
import datetime

class EPReportLevelAdd(EP):

    ID = 'reportlevel_add'
    URL = '/reportlevel/add'

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
        ret['id'] = EPReportLevelAdd.ID
        ret['method'] = EPReportLevelAdd.METHOD
        ret['path-parameter-in-payload'] = EPReportLevelAdd.PATH_PAR_PAYLOAD
        ret['path-parameter-in-url'] = EPReportLevelAdd.PATH_PAR_URL

        ret['parameters'] = [{},{},{}]

        ret['parameters'][0]['attribute'] = EPReportLevelAdd.ATTR_LEVEL_ID
        ret['parameters'][0]['type'] = 'string'
        ret['parameters'][0]['value'] = 1

        ret['parameters'][1]['attribute'] = EPReportLevelAdd.ATTR_VALUE
        ret['parameters'][1]['type'] = 'integer'
        ret['parameters'][1]['min'] = 0
        ret['parameters'][1]['max'] = 100

        ret['parameters'][2]['attribute'] = EPReportLevelAdd.ATTR_VARIANCE
        ret['parameters'][2]['type'] = 'decimal'
        ret['parameters'][2]['min'] = -100
        ret['parameters'][2]['max'] = 100

        return ret

    def executeByParameters(self, levelId, value, variance) -> dict:
        payload = {}
        payload[EPReportLevelAdd.ATTR_LEVEL_ID] = levelId
        payload[EPReportLevelAdd.ATTR_VALUE] = int(value)
        payload[EPReportLevelAdd.ATTR_VARIANCE] = float(variance)
        return self.executeByPayload(payload)


    def executeByPayload(self, payload) -> dict:

        levelId = payload[EPReportLevelAdd.ATTR_LEVEL_ID]
        value = int(payload[EPReportLevelAdd.ATTR_VALUE])
        variance = float(payload[EPReportLevelAdd.ATTR_VARIANCE])

        logging.debug( "WEB request: {0} {1} ('{2}': {3}, '{4}': {5}, '{6}': {7})".format(
                    EPReportLevelAdd.METHOD, EPReportLevelAdd.URL,
                    EPReportLevelAdd.ATTR_LEVEL_ID, levelId,
                    EPReportLevelAdd.ATTR_VALUE, value,
                    EPReportLevelAdd.ATTR_VARIANCE, variance,
                    )
            )

        date = datetime.datetime.now().astimezone().isoformat()
        #self.web_gadget.appendLevelData(date, levelId, value, variance)

        with open(self.web_gadget.reportPath, 'a') as fileObject:
            fileObject.write(f'{date}\t{levelId}\t{value}\t{variance}\n')

        return {'result': 'OK'}

