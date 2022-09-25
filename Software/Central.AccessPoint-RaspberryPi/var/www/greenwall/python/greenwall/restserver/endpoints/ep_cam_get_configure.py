import logging

from greenwall.exceptions.invalid_api_usage import InvalidAPIUsage
from greenwall.restserver.endpoints.ep import EP
from greenwall.restserver.representations import output_json

from flask import request

from dateutil import parser
from datetime import datetime

class EPCamGetConfigure(EP):

    ID = 'cam_configure'
    URL = '/cam/configure'

    PATH_PAR_PAYLOAD = '/configure'
    PATH_PAR_URL = '/configure/ip/<ip>'

    METHOD = 'GET'

    ATTR_IP = 'ip'

#    ATTR_CAM_ID = 'camId'
#    ATTR_CAM_QUALITY = 'camQuality'
#    ATTR_CAM_ROTATE = 'camRotate'
#    ATTR_INTERVAL_FRAME_MILLIS = 'intervalFrameMillis'
#    ATTR_CLIENT_IP = 'clientIp'
#    ATTR_CLIENT_PORT = 'clientPort'

    def __init__(self, web_gadget):
        self.web_gadget = web_gadget

    @staticmethod
    def getRequestDescriptionWithPayloadParameters():

        ret = {}
        ret['id'] = EPCamGetConfigure.ID
        ret['method'] = EPCamGetConfigure.METHOD
        ret['path-parameter-in-payload'] = EPCamGetConfigure.PATH_PAR_PAYLOAD
        ret['path-parameter-in-url'] = EPCamGetConfigure.PATH_PAR_URL

        ret['parameters'] = [{}]

        ret['parameters'][0]['attribute'] = EPCamGetConfigure.ATTR_IP
        ret['parameters'][0]['type'] = 'string'
        ret['parameters'][0]['value'] = 255

        return ret

    def executeByParameters(self, ip) -> dict:
        payload = {}

        payload[EPCamGetConfigure.ATTR_IP] = ip

        return self.executeByPayload(payload)

    def executeByPayload(self, payload) -> dict:

        ip = payload[EPCamGetConfigure.ATTR_IP]

        remoteAddress = request.remote_addr

        logging.debug( "WEB request ({0}): {1} {2} ('{3}': {4})".format(
                    remoteAddress, EPCamGetConfigure.METHOD, EPCamGetConfigure.URL,
                    EPCamGetConfigure.ATTR_IP, ip
                    )
        )

        # Send GET /configure request to the CAM module (identified by the IP)
        ret = self.web_gadget.cam.getConfigure(ip)

        if ret["status"] == 'OK':
            return output_json( ret, EP.CODE_OK)
        else:
            return output_json( ret, EP.CODE_INTERNAL_SERVER_ERROR)
