import logging

from greenwall.exceptions.invalid_api_usage import InvalidAPIUsage
from greenwall.restserver.endpoints.ep import EP
from greenwall.restserver.representations import output_json

from flask import request

from dateutil import parser
from datetime import datetime

class EPSensorTriggerReport(EP):

    ID = 'sensor_trigger_report'
    URL = '/sensor/trigger/report'

    PATH_PAR_PAYLOAD = '/trigger/report'
    PATH_PAR_URL = '/trigger/report'

    METHOD = 'POST'

    ATTR_ID = 'stationId'
    ATTR_CONFIGURE_URL = 'configureUrl'
    ATTR_MEASURE_ACTUAL_URL = 'measureActualUrl'
    ATTR_COLLECT_AVERAGE_URL = 'collectAverageUrl'
    ATTR_DATE_STRING = 'dateString'

    def __init__(self, web_gadget):
        self.web_gadget = web_gadget

    @staticmethod
    def getRequestDescriptionWithPayloadParameters():

        ret = {}
        ret['stationId'] = EPSensorTriggerReport.ID
        ret['method'] = EPSensorTriggerReport.METHOD
        ret['path-parameter-in-payload'] = EPSensorTriggerReport.PATH_PAR_PAYLOAD

        ret['parameters'] = [{},{},{},{},{}]

        ret['parameters'][0]['attribute'] = EPSensorTriggerReport.ATTR_ID
        ret['parameters'][0]['type'] = 'string'
        ret['parameters'][0]['value'] = 255

        ret['parameters'][1]['attribute'] = EPSensorTriggerReport.ATTR_CONFIGURE_URL
        ret['parameters'][1]['type'] = 'string'
        ret['parameters'][1]['value'] = 255

        ret['parameters'][2]['attribute'] = EPSensorTriggerReport.ATTR_MEASURE_ACTUAL_URL
        ret['parameters'][2]['type'] = 'string'
        ret['parameters'][2]['value'] = 255

        ret['parameters'][3]['attribute'] = EPSensorTriggerReport.ATTR_COLLECT_AVERAGE_URL
        ret['parameters'][3]['type'] = 'string'
        ret['parameters'][3]['value'] = 255

        ret['parameters'][4]['attribute'] = EPSensorTriggerReport.ATTR_DATE_STRING
        ret['parameters'][4]['type'] = 'string'
        ret['parameters'][4]['value'] = 255

        return ret

    def executeByParameters(self, stationId=None) -> dict:

        payload = {}
        payload[EPSensorTriggerReport.ATTR_ID] = stationId

        return self.executeByPayload(payload)

    def executeByPayload(self, payload) -> dict:

        stationId = payload[EPSensorTriggerReport.ATTR_ID]

        logging.debug( "SENSOR request: {0} {1} ('{2}': {3} )".format(
                    EPSensorTriggerReport.METHOD, EPSensorTriggerReport.URL,
                    EPSensorTriggerReport.ATTR_ID, stationId,
                    )
            )

        self.web_gadget.sensor.triggerReport(stationId)

        return output_json( {'result': 'OK'}, EP.CODE_OK)

