import logging
from exceptions.invalid_api_usage import InvalidAPIUsage
from restserver.endpoints.ep import EP
from restserver.representations import output_json

from flask import request

from dateutil import parser
from datetime import datetime

class EPLevelAdd(EP):

    ID = 'level_add'
    URL = '/level/add'

    PATH_PAR_PAYLOAD = '/add'
    PATH_PAR_URL = '/add/stationId/<stationId>/dateString/<dateString>/levelValue/<levelValue>/levelVariance/<levelVariance>/temperatureValue/<temperatureValue>/humidityValue/<humidityValue>'

    METHOD = 'POST'

    ATTR_STATION_ID = 'stationId'
    ATTR_DATE_STRING = 'dateString'
    ATTR_LEVEL_VALUE = 'levelValue'
    ATTR_LEVEL_VARIANCE = 'levelVariance'
    ATTR_TEMPERATURE_VALUE = 'temperatureValue'
    ATTR_HUMIDITY_VALUE = 'humidityValue'

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

        ret['parameters'][0]['attribute'] = EPLevelAdd.ATTR_STATION_ID
        ret['parameters'][0]['type'] = 'string'
        ret['parameters'][0]['value'] = 255

        ret['parameters'][1]['attribute'] = EPLevelAdd.ATTR_DATE_STRING
        ret['parameters'][1]['type'] = 'string'
        ret['parameters'][1]['value'] = 255

        ret['parameters'][2]['attribute'] = EPLevelAdd.ATTR_LEVEL_VALUE
        ret['parameters'][2]['type'] = 'decimal'
        ret['parameters'][2]['min'] = 0
        ret['parameters'][2]['max'] = 100

        ret['parameters'][3]['attribute'] = EPLevelAdd.ATTR_LEVEL_VARIANCE
        ret['parameters'][3]['type'] = 'decimal'
        ret['parameters'][3]['min'] = -100
        ret['parameters'][3]['max'] = 100

        ret['parameters'][4]['attribute'] = EPLevelAdd.ATTR_TEMPERATURE_VALUR
        ret['parameters'][4]['type'] = 'decimal'
        ret['parameters'][4]['min'] = -100
        ret['parameters'][4]['max'] = 100

        ret['parameters'][5]['attribute'] = EPLevelAdd.ATTR_HUMIDITY_VALUE
        ret['parameters'][5]['type'] = 'decimal'
        ret['parameters'][5]['min'] = -100
        ret['parameters'][5]['max'] = 100

        return ret

    def executeByParameters(self, stationId, dateString, levelValue, levelVariance, temperatureValue, humidityValue) -> dict:
        payload = {}
        payload[EPLevelAdd.ATTR_STATION_ID] = stationId
        payload[EPLevelAdd.ATTR_DATE_STRING] = dateString
        payload[EPLevelAdd.ATTR_LEVEL_VALUE] = float(levelValue)
        payload[EPLevelAdd.ATTR_LEVEL_VARIANCE] = float(levelVariance)
        payload[EPLevelAdd.ATTR_TEMPERATURE_VALUE] = float(temperatureValue)
        payload[EPLevelAdd.ATTR_HUMIDITY_VALUE] = float(humidityValue)

        return self.executeByPayload(payload)

    def executeByPayload(self, payload) -> dict:

        stationId = payload[EPLevelAdd.ATTR_STATION_ID]
        dateString = payload[EPLevelAdd.ATTR_DATE_STRING]

        try:
            levelValue = float(payload[EPLevelAdd.ATTR_LEVEL_VALUE])
            levelVariance = float(payload[EPLevelAdd.ATTR_LEVEL_VARIANCE])
        except:
            levelVariance = None
            levelValue = None
        try:
            temperatureValue = float(payload[EPLevelAdd.ATTR_TEMPERATURE_VALUE])
            humidityValue = float(payload[EPLevelAdd.ATTR_HUMIDITY_VALUE])
        except:
            temperatureValue = None
            humidityValue = None

        logging.debug( "WEB request: {0} {1} ('{2}': {3}, '{4}': {5}, '{6}': {7}, '{8}':'{9}', '{10}':'{11}', '{12}':'{13}')".format(
                    EPLevelAdd.METHOD, EPLevelAdd.URL,
                    EPLevelAdd.ATTR_STATION_ID, stationId,
                    EPLevelAdd.ATTR_DATE_STRING, dateString,
                    EPLevelAdd.ATTR_LEVEL_VALUE, levelValue,
                    EPLevelAdd.ATTR_LEVEL_VARIANCE, levelVariance,
                    EPLevelAdd.ATTR_TEMPERATURE_VALUE, temperatureValue,
                    EPLevelAdd.ATTR_HUMIDITY_VALUE, humidityValue,
                    )
            )

#        dateString = datetime.now().astimezone().isoformat()
#        dateString = datetime.datetime.now().astimezone().isoformat()

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

        # Report Log
#        with open(self.web_gadget.reportPath, 'a') as fileObject:
#            fileObject.write(f'{dateString}\t{stationId}\t{ip}\t{levelValue}\t{levelVariance}\t{temperatureValue}\t{humidityValue}\n')

        # Add to reportDict
#        print('web_gadget', self.web_gadget, self.web_gadget.report.addRecord )
#        self.web_gadget.report.addRecord(dateString, levelId, ip, value, varinace)
#        print(dateString, levelId, ip, value, variance)
        self.web_gadget.report.addRecordLevel(dateString, stationId, ip, levelValue, levelVariance, temperatureValue, humidityValue)

        # print out to LCD
        self.web_gadget.controlBox.refreshData(stationId)

        return output_json( {'result': 'OK'}, EP.CODE_OK)

