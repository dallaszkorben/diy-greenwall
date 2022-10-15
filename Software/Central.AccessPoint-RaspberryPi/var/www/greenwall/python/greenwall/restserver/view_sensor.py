import json

#from flask_api import status

from flask import Flask
from flask import jsonify
from flask import session
from flask_classful import FlaskView, route, request

from greenwall.config.permanent_data import getPermanentData
from greenwall.config.permanent_data import setPermanentData
from greenwall.config.config import getConfig

from greenwall.exceptions.invalid_api_usage import InvalidAPIUsage

from greenwall.restserver.representations import output_json

from greenwall.restserver.endpoints.ep_sensor_add import EPSensorAdd
from greenwall.restserver.endpoints.ep_sensor_data_list import EPSensorDataList
from greenwall.restserver.endpoints.ep import EP


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
        self.epSensorDataList = EPSensorDataList(web_gadget)

    #
    # GET http://localhost:5000/sensor/
    #
    def index(self):
        return {}

# ===

    #
    # Add sensor data to list with payload
    #
    # curl  --header "Content-Type: application/json" --request POST --data '{"stationId": "5", "levelValue":23.4, "temperatureValue": 12, "humidityValue": 20, "pressureValue": 123}' http://localhost:5000/sensor/add
    #
    # POST http://localhost:5000/sensor/add
    #      body: {
    #        "stationId": "S05",
    #        "levelValue":23.4,
    #        "temperatureValue": 12,
    #        "humidityValue": 20,
    #        "pressureValue": 150
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
    # Add sensor data to list - with parameters
    #
    # New Input structure:
    #	dateString:	NO
    #	sensorVariance:	NO
    #	pressureValue:	YES
    #
    # curl  --header "Content-Type: application/json" --request POST http://localhost:5000/sensor/add/stationId/5/levelValue/23.4/temperatureValue/12/humidityValue/2/pressureValue/123
    #
    # POST http://localhost:5000/sensor/add/stationId/5/levelValue/23.4/teperatureValue/12/humidityValue/2/pressureValue/123
    #
    #@route('/add/stationId/<stationId>/levelValue/<levelValue>/temperatureValue/<temperatureValue>/humidityValue/<humidityValue>/pressureValue/<pressureValue>, methods=['POST'])
    @route(EPSensorAdd.PATH_PAR_URL, methods=[EPSensorAdd.METHOD])
    def setWithParameter(self, stationId, levelValue, temperatureValue, humidityValue, pressureValue):

        out = self.epSensorAdd.executeByParameters(stationId=stationId, levelValue=levelValue, temperatureValue=temperatureValue, humidityValue=humidityValue, pressureValue=pressureValue)
        return out


# ===

# ===

    #
    # Fetch sensor data - with parameters
    #
    # curl  --header "Content-Type: application/json" --request GET http://localhost:5000/sensor/data/list/startDate/2021.11.07T20:15:123+01:00
    #
    # READ http://localhost:5000/sensor/data/list/startDate/2021.11.07T20:15:123+01:00
    #
    #@route('/data/list/startDate/<startDate>', methods=['GET'])
    @route(EPSensorDataList.PATH_PAR_1_URL, methods=[EPSensorDataList.METHOD])
    def dataListWith1Parameter(self, startDate):

        out = self.epSensorDataList.executeByParameters(startDate=startDate)
        return out

    #
    # Fetch sensor data - with parameters
    #
    # curl  --header "Content-Type: application/json" --request GET http://localhost:5000/sensor/data/list/startDate/2021.11.07T20:15:123+01:00/endDate/2021.11.08T20:15:123+01:00
    #
    # READ http://localhost:5000/sensor/data/list/startDate/2021.11.07T20:15:123+01:00
    #
    #@route('/data/list/startDate/<startDate>/endDate/<endDate>', methods=['GET'])
    @route(EPSensorDataList.PATH_PAR_2_URL, methods=[EPSensorDataList.METHOD])
    def dataListWith2Parameters(self, startDate, endDate):

        out = self.epSensorDataList.executeByParameters(startDate=startDate, endDate=endDate)
        return out

