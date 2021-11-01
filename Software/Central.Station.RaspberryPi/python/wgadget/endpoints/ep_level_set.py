
import logging
from exceptions.invalid_api_usage import InvalidAPIUsage
from wgadget.endpoints.ep import EP

class EPLevelSet(EP):

    NAME = 'set_level'
    URL = '/level/set'

    URL_ROUTE_PAR_PAYLOAD = '/set'
    URL_ROUTE_PAR_URL = '/set/levelId/<levelId>/value/<value>/variance/<variance>'

    METHOD = 'POST'

    ATTR_LEVEL_ID = 'levelId'
    ATTR_VALUE = 'value'
    ATTR_VARIANCE = 'variance'

    def __init__(self, web_gadget):
        self.web_gadget = web_gadget

    def getRequestDescriptionWithPayloadParameters(self):

        ret = {}
        ret['name'] = EPLevelSet.NAME
        ret['url'] = EPLevelSet.URL_ROUTE_PAR_PAYLOAD
        ret['method'] = EPLevelSet.METHOD

        ret['payload-desc'] = [{},{}]

        ret['payload-desc'][0]['attribute'] = EPLevelSet.ATTR_LEVEL_ID
        ret['payload-desc'][0]['type'] = 'string'
        ret['payload-desc'][0]['value'] = 1


        ret['payload-desc'][1]['attribute'] = EPLevelSet.ATTR_VALUE
        ret['payload-desc'][1]['type'] = 'integer'
        ret['payload-desc'][1]['min'] = 0
        ret['payload-desc'][1]['max'] = 100

        ret['payload-desc'][2]['attribute'] = EPLevelSet.ATTR_VARIANCE
        ret['payload-desc'][2]['type'] = 'decimal'
        ret['payload-desc'][2]['min'] = -100
        ret['payload-desc'][2]['max'] = 100

        return ret

    def executeByParameters(self, levelId, value, variance) -> dict:
        payload = {}
        payload[EPLevelSet.ATTR_LEVEL_ID] = levelId
        payload[EPLevelSet.ATTR_VALUE] = int(value)
        payload[EPLevelSet.ATTR_VARIANCE] = float(variance)
        return self.executeByPayload(payload)


    def executeByPayload(self, payload) -> dict:

        levelId = payload[EPLevelSet.ATTR_LEVEL_ID]
        value = int(payload[EPLevelSet.ATTR_VALUE])
        variance = float(payload[EPLevelSet.ATTR_VARIANCE])

        logging.debug( "WEB request: {0} {1} ('{2}': {3}, '{4}': {5}, '{6}': {7})".format(
                    EPLevelSet.METHOD, EPLevelSet.URL,
                    EPLevelSet.ATTR_LEVEL_ID, levelId,
                    EPLevelSet.ATTR_VALUE, value,
                    EPLevelSet.ATTR_VARIANCE, variance,
                    )
            )

        return {'result': 'OK'}

#        print( "WEB request: {0} {1} ('{2}': {3}, '{4}': {5}, '{6}': {7})".format(
#                    EPLevelSet.METHOD, EPLevelSet.URL,
#                    EPLevelSet.ATTR_LEVEL_ID, levelId,
#                    EPLevelSet.ATTR_VALUE, value,
#                    EPLevelSet.ATTR_VARIANCE, variance,
#                    )
#            )
