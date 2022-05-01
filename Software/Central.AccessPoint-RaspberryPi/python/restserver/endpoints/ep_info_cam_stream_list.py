import logging
from exceptions.invalid_api_usage import InvalidAPIUsage
from restserver.endpoints.ep import EP
from flask import request
from restserver.representations import output_json

from dateutil import parser
from datetime import datetime

import numpy as np
from utilities.register_cam_stream import RegisterCamStream

from scipy import stats

class EPInfoCamStreamList(EP):

    ID = 'info_cam_stream_list'
    URL = '/info/camStreamList'

    PATH_PAR_PAYLOAD = '/camStreamList'
    PATH_PAR_URL = '/camstreamList'

    METHOD = 'GET'

    def __init__(self, web_gadget):
        self.web_gadget = web_gadget

    @staticmethod
    def getRequestDescriptionWithPayloadParameters():

        ret = {}
        ret['id'] = EPInfoCamStreamList.ID
        ret['method'] = EPInfoCamStreamList.METHOD
        ret['path-parameter-in-payload'] = EPInfoCamStreamList.PATH_PAR_PAYLOAD
        ret['path-parameter-in-url'] = EPInfoCamStreamList.PATH_PAR_URL

        ret['parameters'] = [{}]

#        ret['parameters'][0]['attribute'] = EPInfoTimeStamp.ATTR_START_DATE
#        ret['parameters'][0]['type'] = 'date'
#        ret['parameters'][0]['min'] = datetime.datetime(2000, 1,1).astimezone().isoformat()
#        ret['parameters'][0]['max'] = datetime.datetime.now().astimezone().isoformat()

        return ret

    def executeByParameters(self) -> dict:

        payload = {}
        return self.executeByPayload(payload)

    def executeByPayload(self, payload) -> dict:

        logging.debug( "WEB request: {0} {1} ()".format(
                    EPInfoCamStreamList.METHOD, EPInfoCamStreamList.URL,
                )
        )

        camStreamList = self.web_gadget.registerCamStream.getValueList()

        ret = {"result": "OK", "camStreamList": camStreamList}
        return output_json( ret, EP.CODE_OK)

