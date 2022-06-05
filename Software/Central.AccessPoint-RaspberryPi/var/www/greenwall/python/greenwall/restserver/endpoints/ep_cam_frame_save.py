import logging

from greenwall.exceptions.invalid_api_usage import InvalidAPIUsage
from greenwall.restserver.endpoints.ep import EP
from greenwall.restserver.representations import output_json

from flask import request

from dateutil import parser
from datetime import datetime

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 

class EPCamFrameSave(EP):

    ID = 'cam_frame_save'
    URL = '/cam/frame/save'

    PATH_PAR_PAYLOAD = '/frame/save'
    PATH_PAR_URL = '/frame/save/camId/<camId>/timestamp/<timestamp>'

    METHOD = 'POST'

    ATTR_CAM_ID = 'camId'
    ATTR_TIMESTAMP = 'timestamp'
    ATTR_IMAGE = 'image'

    def __init__(self, web_gadget):
        self.web_gadget = web_gadget

    @staticmethod
    def getRequestDescriptionWithPayloadParameters():

        ret = {}
        ret['id'] = EPCamAdd.ID
        ret['method'] = EPCamFrameSave.METHOD
        ret['path-parameter-in-payload'] = EPCamFrameSave.PATH_PAR_PAYLOAD
        ret['path-parameter-in-url'] = EPCamFrameSave.PATH_PAR_URL

        ret['parameters'] = [{},{},{}]

        ret['parameters'][0]['attribute'] = EPCamFrameSave.ATTR_CAM_ID
        ret['parameters'][0]['type'] = 'string'
        ret['parameters'][0]['value'] = 255

        ret['parameters'][1]['attribute'] = EPCamFrameSave.ATTR_TIMESTAMP
        ret['parameters'][1]['type'] = 'string'
        ret['parameters'][1]['value'] = 255

        return ret

    def executeByParameters(self, camId, timestamp, image) -> dict:
        payload = {}
        payload[EPCamFrameSave.ATTR_CAM_ID] = camId
        payload[EPCamFrameSave.ATTR_TIMESTAMP] = timestamp
        payload[EPCamFrameSave.ATTR_IMAGE] = image

        return self.executeByPayload(payload)

    def executeByPayload(self, payload) -> dict:

        camId = payload[EPCamFrameSave.ATTR_CAM_ID]
        timestamp = payload[EPCamFrameSave.ATTR_TIMESTAMP]
        image = payload[EPCamFrameSave.ATTR_IMAGE]

        date = parser.parse(timestamp)
        dateString = date.astimezone().isoformat()

        webFolderName = self.web_gadget.webFolderName
        webPathNameCamFrame = self.web_gadget.webPathNameCamFrame

        fileName = f'{camId}-{timestamp}.jpg'

        fileNamePath = f'{webFolderName}/{webPathNameCamFrame}/{fileName}'


        if image:
            logging.debug( "WEB request: {0} {1} ('{2}': {3}, '{4}': {5}, '{6}': {7}, '{8}': {9})".format(
                    EPCamFrameSave.METHOD, EPCamFrameSave.URL,
                    EPCamFrameSave.ATTR_CAM_ID, camId,
                    EPCamFrameSave.ATTR_TIMESTAMP, timestamp,
                    EPCamFrameSave.ATTR_IMAGE, image,
                    "FilenamePath", fileNamePath
                    )
            )

            img = Image.open(image)

            # add timestamp to the image
            draw = ImageDraw.Draw(img)
            font = ImageFont.truetype("DejaVuSans.ttf", 32)
            draw.text((0,20), dateString, (100,100,100), font=font)

            print('before save')
            img.save(fileNamePath)
            print('after save')

            print(f'{fileNamePath} file saved')

            return output_json( {'result': 'OK'}, EP.CODE_OK)

        else:

            logging.debug( "WEB request: {0} {1} ('{2}': {3}, '{4}': {5}, '{6}': {7})".format(
                    EPCamFrameSave.METHOD, EPCamFrameSave.URL,
                    EPCamFrameSave.ATTR_CAM_ID, camId,
                    EPCamFrameSave.ATTR_TIMESTAMP, timestamp,
                    EPCamFrameSave.ATTR_IMAGE, image
                    )
            )

            print("!!! No file was saved")
            return output_json( {'result': 'ERROR'}, EP.CODE_BAD_REQUEST)

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

#        ip = request.remote_addr

        # Report Log

        # Add to reportDict
#        self.web_gadget.reportSensor.addRecordSensor(dateString, stationId, ip, levelValue, levelVariance, temperatureValue, humidityValue)

        # print out to LCD
#        self.web_gadget.controlBox.refreshData(stationId)



