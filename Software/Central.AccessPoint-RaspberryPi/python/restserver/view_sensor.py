import json

#from flask_api import status

from flask import Flask
from flask import jsonify
from flask import session
from flask_classful import FlaskView, route, request

from restserver.representations import output_json

from config.permanent_data import getPermanentData
from config.permanent_data import setPermanentData
from config.config import getConfig

from exceptions.invalid_api_usage import InvalidAPIUsage

from restserver.endpoints.ep_sensor_add import EPSensorAdd

from restserver.endpoints.ep import EP


# -----------------------------------
#
# POST Contorl the sensor of the light
#
# curl  --header "Content-Type: application/json" --request POST http://localhost:5000/sensor/add/sensorId/5/value/23.4/variance/0.0
# curl  --header "Content-Type: application/json" --request POST --data '{"sensorId": "5", "value":23.4,"variance":0.0}' http://localhost:5000/sensor/add
#
# -----------------------------------
#
# POST http://localhost:5000/sensor
class SensorView(FlaskView):
    representations = {'application/json': output_json}
    inspect_args = False

    def __init__(self, web_gadget):

        self.web_gadget = web_gadget

        self.epSensorAdd = EPSensorAdd(web_gadget)

    #
    # GET http://localhost:5000/sensor/
    #
    def index(self):
        return {}

# ===

    #
    # Set the sensor with payload
    #
    # curl  --header "Content-Type: application/json" --request POST --data '{"stationId": "5", "dateString": "2021.12.03T11:34", "levelValue":23.4, "sensorVariance":0.0 "temperatureValue": 12, "humidityValue": 20}' http://localhost:5000/sensor/add
    #
    # POST http://localhost:5000/sensor/add
    #      body: {
    #        "stationId": "5",
    #        "dateString": "2021.12.03T11:34",
    #        "levelValue":23.4,
    #        "levelVariance":0.0
    #        "temperatureValue": 12,
    #        "humidityValue": 20
    #      }
    #
    #@route('/add', methods=['POST'])
    @route(EPSensorAdd.PATH_PAR_PAYLOAD, methods=[EPSensorAdd.METHOD])
    def setWithPayload(self):

        # WEB
        if request.form:
            json_data = request.form

        # CURL
        elif request.json:
            json_data = request.json

        else:
            return "Not valid request", EP.CODE_BAD_REQUEST

        out = self.epSensorAdd.executeByPayload(json_data)
        return out

    #
    # Read the sensor - with parameters
    #
    # curl  --header "Content-Type: application/json" --request POST http://localhost:5000/sensor/add/stationId/5/dateString/2021.12.03T11:34/levelValue/23.4/sensorVariance/0.0/temperatureValue/12/humidityValue/2
    #
    # POST http://localhost:5000/sensor/add/stationId/5/dateString/2021.12.03T11:34/levelValue/23.4/sensorVariance/0.0/teperatureValue/12/humidityValue/2
    #
    #@route('/add/stationId/<stationId>/dateString/<dateString>/levelValue/<levelValue>/sensorVariance/<sensorVariance>/temperatureValue/<temperatureValue>/humidityValue/<humidityValue>, methods=['POST'])
    @route(EPSensorAdd.PATH_PAR_URL, methods=[EPSensorAdd.METHOD])
    def setWithParameter(self, stationId, dateString, levelValue, levelVariance, temperatureValue, humidityValue):

        out = self.epSensorAdd.executeByParameters(stationId=stationId, levelValue=levelValue, levelVariance=levelVariance, temperatureValue=temperatureValue, humidityValue=humidityValue)
        return out








# ===

    #
    # Read the sensor - with payload
    #
    # curl  --header "Content-Type: application/json" --request GET --data '{"startDate":"2021.11.07T20:15:123+01:00"}' http://localhost:5000/sensor/read
    #
    # GET http://localhost:5000/sensor/read
    #      body: {
    #            "startDate":"2021.11.07T20:15:123+01:00"
    #           }
    #
    #@route('/read', methods=['GET'])
#    @route(EPInfoSensor.PATH_PAR_PAYLOAD, methods=[EPInfoSensor.METHOD])
#    def readWithPayload(self):
#
#        # WEB
#        if request.form:
#            json_data = request.form
#
#        # CURL
#        elif request.json:
#            json_data = request.json
#
#        else:
#            return "Not valid request", EP.CODE_BAD_REQUEST
#
#        out = self.epInfoSensor.executeByPayload(json_data)
#        return out

    #
    # Read the sensor - with parameters
    #
    # curl  --header "Content-Type: application/json" --request GET http://localhost:5000/sensor/read/startDate/2021.11.07T20:15:123+01:00
    #
    # READ http://localhost:5000/sensor/read/startDate/2021.11.07T20:15:123+01:00
    #
    #@route('/read/startDate/<startDate>', methods=['GET'])
#    @route(EPInfoSensor.PATH_PAR_URL, methods=[EPInfoSensor.METHOD])
#    def readWithParameter(self, startDate):
#
#        out = self.epInfoSensor.executeByParameters(startDate=startDate)
#        return out


# ===

