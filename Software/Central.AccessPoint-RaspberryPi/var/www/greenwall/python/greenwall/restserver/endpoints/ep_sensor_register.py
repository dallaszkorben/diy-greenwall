import logging

from greenwall.exceptions.invalid_api_usage import InvalidAPIUsage
from greenwall.restserver.endpoints.ep import EP
from greenwall.restserver.representations import output_json

from flask import request

from dateutil import parser
from datetime import datetime

class EPSensorRegister(EP):

    ID = 'sensor_register'
    URL = '/sensor/register'

    PATH_PAR_PAYLOAD = '/register'
#    PATH_PAR_URL = '/stream/register/dateString/<dateString>/stationId/<stationId>'

    METHOD = 'POST'

    ATTR_ID = 'stationId'
    ATTR_CONFIGURE_URL = 'configureUrl'
    ATTR_MEASURE_ACTUAL_URL = 'measureActualUrl'
    ATTR_COLLECT_AVERAGE_URL = 'collectAverageUrl'
    ATTR_TRIGGER_REPORT_URL = 'triggerReportUrl'
    ATTR_DATE_STRING = 'dateString'

    def __init__(self, web_gadget):
        self.web_gadget = web_gadget

    @staticmethod
    def getRequestDescriptionWithPayloadParameters():

        ret = {}
        ret['stationId'] = EPSensorRegister.ID
        ret['method'] = EPSensorRegister.METHOD
        ret['path-parameter-in-payload'] = EPSensorRegister.PATH_PAR_PAYLOAD

        ret['parameters'] = [{},{},{},{},{}]

        ret['parameters'][0]['attribute'] = EPSensorRegister.ATTR_ID
        ret['parameters'][0]['type'] = 'string'
        ret['parameters'][0]['value'] = 255

        ret['parameters'][1]['attribute'] = EPSensorRegister.ATTR_CONFIGURE_URL
        ret['parameters'][1]['type'] = 'string'
        ret['parameters'][1]['value'] = 255

        ret['parameters'][2]['attribute'] = EPSensorRegister.ATTR_MEASURE_ACTUAL_URL
        ret['parameters'][2]['type'] = 'string'
        ret['parameters'][2]['value'] = 255

        ret['parameters'][3]['attribute'] = EPSensorRegister.ATTR_COLLECT_AVERAGE_URL
        ret['parameters'][3]['type'] = 'string'
        ret['parameters'][3]['value'] = 255

        ret['parameters'][4]['attribute'] = EPSensorRegister.ATTR_TRIGGER_REPORT_URL
        ret['parameters'][4]['type'] = 'string'
        ret['parameters'][4]['value'] = 255

        ret['parameters'][5]['attribute'] = EPSensorRegister.ATTR_DATE_STRING
        ret['parameters'][5]['type'] = 'string'
        ret['parameters'][5]['value'] = 255

        return ret

    def executeByParameters(self, stationId, configureUrl, measureActualUrl, collectAverageUrl, triggerReportUrl, dateString) -> dict:
        payload = {}
        payload[EPSensorRegister.ATTR_ID] = stationId
        payload[EPSensorRegister.ATTR_CONFIGURE_URL] = configureUrl
        payload[EPSensorRegister.ATTR_MEASURE_ACTUAL_URL] = measureActualUrl
        payload[EPSensorRegister.ATTR_COLLECT_AVERAGE_URL] = collectAverageUrl
        payload[EPSensorRegister.ATTR_TRIGGER_REPORT_URL] = triggerReportUrl
        payload[EPSensorRegister.ATTR_DATE_STRING] = dateString

        return self.executeByPayload(payload)

    def executeByPayload(self, payload) -> dict:

        stationId = payload[EPSensorRegister.ATTR_ID]
        configureUrl = payload[EPSensorRegister.ATTR_CONFIGURE_URL]
        measureActualUrl = payload[EPSensorRegister.ATTR_MEASURE_ACTUAL_URL]
        collectAverageUrl = payload[EPSensorRegister.ATTR_COLLECT_AVERAGE_URL]
        triggerReportUrl = payload[EPSensorRegister.ATTR_TRIGGER_REPORT_URL]
        dateString = payload[EPSensorRegister.ATTR_DATE_STRING]

        logging.debug( "SENSOR request: {0} {1} ('{2}': {3}, '{4}': {5}, '{6}': {7}, '{8}': {9}, '{10}': {11}, '{12}': {13} )".format(
                    EPSensorRegister.METHOD, EPSensorRegister.URL,
                    EPSensorRegister.ATTR_ID, stationId,
                    EPSensorRegister.ATTR_CONFIGURE_URL, configureUrl,
                    EPSensorRegister.ATTR_MEASURE_ACTUAL_URL, measureActualUrl,
                    EPSensorRegister.ATTR_COLLECT_AVERAGE_URL, collectAverageUrl,
                    EPSensorRegister.ATTR_TRIGGER_REPORT_URL, triggerReportUrl,
                    EPSensorRegister.ATTR_DATE_STRING, dateString
                    )
            )

        date = parser.parse(dateString)
        dateString = date.astimezone().isoformat()

        stationIp = request.remote_addr

        self.web_gadget.registerSensor.register(dateString, stationIp, stationId, configureUrl, measureActualUrl, collectAverageUrl, triggerReportUrl)

        # print out to LCD
#        self.web_gadget.controlBox.refreshData(stationId)

        return output_json( {'result': 'OK'}, EP.CODE_OK)

