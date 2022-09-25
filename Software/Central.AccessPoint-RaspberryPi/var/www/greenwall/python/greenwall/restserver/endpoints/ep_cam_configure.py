import logging

from greenwall.exceptions.invalid_api_usage import InvalidAPIUsage
from greenwall.restserver.endpoints.ep import EP
from greenwall.restserver.representations import output_json

from flask import request

from dateutil import parser
from datetime import datetime

class EPCamConfigure(EP):
    """
        Input parameters:
            ip:                     Mandatory
            camId:                  Optional - can be any text
            camQuality:             Optional - 96X96,QQVGA,QCIF,HQVGA,240X240,QVGA,CIF,HVGA,VGA,SVGA,XGA,HD,SXGA,UXGA
            camRotate:              Optional - 0, 1, 2, 3
            intervalFrameMillis:    Optional - 
            clientIp:               Optional -
            clientPort:             Optional -
    """

    ID = 'cam_configure'
    URL = '/cam/configure'

    PATH_PAR_PAYLOAD = '/configure'
    PATH_PAR_URL = '/configure'

    METHOD = 'POST'

    ATTR_IP = 'ip'
    ATTR_CAM_ID = 'camId'
    ATTR_CAM_QUALITY = 'camQuality'
    ATTR_CAM_ROTATE = 'camRotate'
    ATTR_INTERVAL_FRAME_MILLIS = 'intervalFrameMillis'
    ATTR_CLIENT_IP = 'clientIp'
    ATTR_CLIENT_PORT = 'clientPort'

    def __init__(self, web_gadget):
        self.web_gadget = web_gadget

    @staticmethod
    def getRequestDescriptionWithPayloadParameters():

        ret = {}
        ret['id'] = EPCamConfigure.ID
        ret['method'] = EPCamConfigure.METHOD
        ret['path-parameter-in-payload'] = EPCamConfigure.PATH_PAR_PAYLOAD
        ret['path-parameter-in-url'] = EPCamConfigure.PATH_PAR_URL

        ret['parameters'] = [{},{},{},{},{},{},{}]

        ret['parameters'][0]['attribute'] = EPCamConfigure.ATTR_IP
        ret['parameters'][0]['type'] = 'string'
        ret['parameters'][0]['value'] = 255

        ret['parameters'][1]['attribute'] = EPCamConfigure.ATTR_CAM_ID
        ret['parameters'][1]['type'] = 'string'
        ret['parameters'][1]['value'] = 255

        ret['parameters'][2]['attribute'] = EPCamConfigure.ATTR_CAM_QUALITY
        ret['parameters'][2]['type'] = 'string'
        ret['parameters'][2]['value'] = 255

        ret['parameters'][3]['attribute'] = EPCamConfigure.ATTR_CAM_ROTATE
        ret['parameters'][3]['type'] = 'string'
        ret['parameters'][3]['value'] = 255

        ret['parameters'][4]['attribute'] = EPCamConfigure.ATTR_INTERVAL_FRAME_MILLIS
        ret['parameters'][4]['type'] = 'string'
        ret['parameters'][4]['value'] = 255

        ret['parameters'][5]['attribute'] = EPCamConfigure.ATTR_CLIENT_IP
        ret['parameters'][5]['type'] = 'string'
        ret['parameters'][5]['value'] = 255

        ret['parameters'][6]['attribute'] = EPCamConfigure.ATTR_CLIENT_PORT
        ret['parameters'][6]['type'] = 'string'
        ret['parameters'][6]['value'] = 255

        return ret

    def executeByParameters(self, ip, camId=None, camQuality=None, camRotate=None, intervalFrameMillis=None, clientIp=None, clientPort=None) -> dict:
        payload = {}

        payload[EPCamConfigure.ATTR_IP] = ip
        payload[EPCamConfigure.ATTR_CAM_ID] = camId
        payload[EPCamConfigure.ATTR_CAM_QUALITY] = camQuality
        payload[EPCamConfigure.ATTR_CAM_ROTATE] = camRotate
        payload[EPCamConfigure.ATTR_INTERVAL_FRAME_MILLIS] = intervalFrameMillis
        payload[EPCamConfigure.ATTR_CLIENT_IP] = clientIp
        payload[EPCamConfigure.ATTR_CLIENT_PORT] = clientPort

        return self.executeByPayload(payload)

    def executeByPayload(self, payload) -> dict:

        ip = payload[EPCamConfigure.ATTR_IP]

        if EPCamConfigure.ATTR_CAM_ID in payload:
            camId = payload[EPCamConfigure.ATTR_CAM_ID]
        else:
            camId = None

        if EPCamConfigure.ATTR_CAM_QUALITY in payload:
            camQuality = payload[EPCamConfigure.ATTR_CAM_QUALITY]
        else:
            camQuality = None

        if EPCamConfigure.ATTR_CAM_ROTATE in payload:
            camRotate = payload[EPCamConfigure.ATTR_CAM_ROTATE]
        else:
            camRotate = None

        if EPCamConfigure.ATTR_INTERVAL_FRAME_MILLIS in payload:
            intervalFrameMillis = payload[EPCamConfigure.ATTR_INTERVAL_FRAME_MILLIS]
        else:
            intervalFrameMillis = None

        if EPCamConfigure.ATTR_CLIENT_IP in payload:
            clientIp = payload[EPCamConfigure.ATTR_CLIENT_IP]
        else:
            clientIp = None

        if EPCamConfigure.ATTR_CLIENT_PORT in payload:
            clientPort = payload[EPCamConfigure.ATTR_CLIENT_PORT]
        else:
            clientPort = None

        remoteAddress = request.remote_addr

        logging.debug( "WEB request ({0}): {1} {2} ('{3}': {4}, '{5}': {6}, '{7}': {8}, '{9}': {10}, '{11}': {12}, '{13}': {14}, '{15}': {16})".format(
                    remoteAddress, EPCamConfigure.METHOD, EPCamConfigure.URL,
                    EPCamConfigure.ATTR_IP, ip,
                    EPCamConfigure.ATTR_CAM_ID, camId,
                    EPCamConfigure.ATTR_CAM_QUALITY, camQuality,
                    EPCamConfigure.ATTR_CAM_ROTATE, camRotate,
                    EPCamConfigure.ATTR_INTERVAL_FRAME_MILLIS, intervalFrameMillis,
                    EPCamConfigure.ATTR_CLIENT_IP, clientIp,
                    EPCamConfigure.ATTR_CLIENT_PORT, clientPort
                    )
        )

        # Send POST /configure request to the CAM module (identified by the IP)
        result = self.web_gadget.cam.postConfigure(ip, camId, camQuality, camRotate, intervalFrameMillis, clientIp, clientPort)

        if result['status'] == 'OK':
            return output_json( result, EP.CODE_OK)
        else:
            return output_json( result, EP.CODE_INTERNAL_SERVER_ERROR)

