from threading import Thread
from datetime import datetime
from exceptions.invalid_api_usage import InvalidAPIUsage
import logging
from wgadget.endpoints.ep import EP

class EPGraduallyScheduleSetLight(EP):

    NAME = 'scheduled_set_light_gradually'
    URL = '/gradually/schedule/set'

    URL_ROUTE_PAR_PAYLOAD = '/schedule/set'
    URL_ROUTE_PAR_URL = '/schedule/set/actuatorId/<actuatorId>/value/<value>/inSeconds/<inSeconds>/atDateTime/<atDateTime>'

    METHOD = 'POST'

    ATTR_ACTUATOR_ID = 'actuatorId'
    ATTR_VALUE = 'value'
    ATTR_IN_SECONDS = 'inSeconds'
    ATTR_AT_DATE_TIME = 'atDateTime'

    def __init__(self, web_gadget):
        self.web_gadget = web_gadget

    def getRequestDescriptionWithPayloadParameters(self):

        ret = {}
        ret['name'] = EPGraduallyScheduleSetLight.NAME
        ret['url'] = EPGraduallyScheduleSetLight.URL_ROUTE_PAR_PAYLOAD
        ret['method'] = EPGraduallyScheduleSetLight.METHOD

        ret['payload-desc'] = [{},{},{},{}]

        ret['payload-desc'][0]['attribute'] = EPGraduallyScheduleSetLight.ATTR_ACTUATOR_ID
        ret['payload-desc'][0]['type'] = 'integer'
        ret['payload-desc'][0]['value'] = 1


        ret['payload-desc'][1]['attribute'] = EPGraduallyScheduleSetLight.ATTR_VALUE
        ret['payload-desc'][1]['type'] = 'integer'
        ret['payload-desc'][1]['min'] = 0
        ret['payload-desc'][1]['max'] = 100

        ret['payload-desc'][2]['attribute'] = EPGraduallyScheduleSetLight.ATTR_IN_SECONDS
        ret['payload-desc'][2]['type'] = 'integer'
        ret['payload-desc'][2]['min'] = 0
        ret['payload-desc'][2]['max'] = None

        ret['payload-desc'][3]['attribute'] = EPGraduallyScheduleSetLight.ATTR_AT_DATE_TIME
        ret['payload-desc'][3]['type'] = 'string'

        return ret

    def executeByParameters(self, actuatorId, value, inSeconds, atDateTime):
        payload = {}
        payload[EPGraduallyScheduleSetLight.ATTR_ACTUATOR_ID] = int(actuatorId)
        payload[EPGraduallyScheduleSetLight.ATTR_VALUE] = int(value)
        payload[EPGraduallyScheduleSetLight.ATTR_IN_SECONDS] = int(inSeconds)
        payload[EPGraduallyScheduleSetLight.ATTR_AT_DATE_TIME] = atDateTime
        self.executeByPayload(payload)


    def executeByPayload(self, payload):

        actuatorId = int(payload[EPGraduallyScheduleSetLight.ATTR_ACTUATOR_ID])
        value = int(payload[EPGraduallyScheduleSetLight.ATTR_VALUE])
        inSeconds = int(payload[EPGraduallyScheduleSetLight.ATTR_IN_SECONDS])
        atDateTime = datetime.fromisoformat(payload[EPGraduallyScheduleSetLight.ATTR_AT_DATE_TIME])

        if actuatorId == self.web_gadget.getLightId():

            if value >= 0 and value <= 100:

                logging.debug( "WEB request: {0} {1} ('{2}': {3}, '{4}': {5}, '{6}': {7}, '{8}': {9})".format(
                    EPGraduallyScheduleSetLight.METHOD, EPGraduallyScheduleSetLight.URL,
                    EPGraduallyScheduleSetLight.ATTR_ACTUATOR_ID, actuatorId,
                    EPGraduallyScheduleSetLight.ATTR_VALUE, value,
                    EPGraduallyScheduleSetLight.ATTR_IN_SECONDS, inSeconds,
                    EPGraduallyScheduleSetLight.ATTR_AT_DATE_TIME, atDateTime)
                )

                # Save the light value and set the Light
                thread = Thread(target = self.web_gadget.setLightScheduledGradually, args = (value, inSeconds, atDateTime)) 
                thread.daemon = True
                thread.start()

            else:
                raise InvalidAPIUsage("The value is not valid: {0}".format(value), status_code=404)

        else:
            raise InvalidAPIUsage("No such actuator: {0} or value: {1} or in_seconds: {2} or at: {3}".format(actuator, value, inSeconds, atDateTime), status_code=404)

        return {'status': 'OK'}


