import logging

from greenwall.exceptions.invalid_api_usage import InvalidAPIUsage
from greenwall.restserver.endpoints.ep import EP
from greenwall.restserver.representations import output_json

from flask import request

from dateutil import parser
from datetime import datetime
from datetime import timedelta

import numpy as np

from scipy import stats

class EPInfoTimeStamp(EP):

    ID = 'info_timestamp'
    URL = '/info/timeStamp'

    PATH_PAR_PAYLOAD = '/timeStamp'
    PATH_PAR_URL = '/timeStamp/epocDate/<epocDate>'

    METHOD = 'GET'

    ATTR_EPOC_DATE = 'epocDate'

    def __init__(self, web_gadget):
        self.web_gadget = web_gadget

    @staticmethod
    def getRequestDescriptionWithPayloadParameters():

        ret = {}
        ret['id'] = EPInfoTimeStamp.ID
        ret['method'] = EPInfoTimeStamp.METHOD
        ret['path-parameter-in-payload'] = EPInfoTimeStamp.PATH_PAR_PAYLOAD
        ret['path-parameter-in-url'] = EPInfoTimeStamp.PATH_PAR_URL

        ret['parameters'] = [{}]

        ret['parameters'][0]['attribute'] = EPInfoTimeStamp.ATTR_START_DATE
        ret['parameters'][0]['type'] = 'date'
        ret['parameters'][0]['min'] = datetime.datetime(2000, 1,1).astimezone().isoformat()
        ret['parameters'][0]['max'] = datetime.datetime.now().astimezone().isoformat()

        return ret

    def executeByParameters(self, epocDate) -> dict:

        payload = {}
        payload[EPInfoTimeStamp.ATTR_EPOC_DATE] = epocDate
        return self.executeByPayload(payload)

    def executeByPayload(self, payload) -> dict:

        parameterEpocDateString = payload[EPInfoTimeStamp.ATTR_EPOC_DATE]

        epocDateString = parser.parse(parameterEpocDateString).astimezone().isoformat()
        epocDateTime = parser.parse(epocDateString)
        epocDateStamp = datetime.timestamp(epocDateTime)

        logging.debug( "SENSOR request: {0} {1} ('{2}': {3})".format(
                    EPInfoTimeStamp.METHOD, EPInfoTimeStamp.URL,
                    EPInfoTimeStamp.ATTR_EPOC_DATE, epocDateString
                )
        )

        todaynow=datetime.now()
        timezone =todaynow.astimezone()

        delta=timezone.utcoffset()
        offsetString=correct_offset(delta)

        localNowDateStamp = todaynow.astimezone().timestamp()
        returnTimeStamp = localNowDateStamp - epocDateStamp

        ret = {"result": "OK", "timeStamp": int(returnTimeStamp), "offsetInt": delta.seconds, "offsetString": offsetString}
        return output_json( ret, EP.CODE_OK)


def correct_offset(delta):
    if delta.days < 0:
        delta = timedelta() - delta
    
        offsettime=datetime.strptime(str(delta),'%H:%M:%S').time()
        offsetstring=offsettime.strftime('%H:%M')
        full_delta = "-{0}".format(offsetstring)
    else:
        offsettime=datetime.strptime(str(delta),'%H:%M:%S').time()
        offsetstring=offsettime.strftime('%H:%M')
        full_delta = "+{0}".format(offsetstring)
    return full_delta
