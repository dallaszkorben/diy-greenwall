import logging

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
from greenwall.restserver.endpoints.ep_sensor_register import EPSensorRegister
from greenwall.restserver.endpoints.ep_sensor_data_list import EPSensorDataList

from greenwall.restserver.endpoints.ep_sensor_registered_list import EPSensorRegisteredList
from greenwall.restserver.endpoints.ep_sensor_data_average_by_id import EPSensorDataAverageById
from greenwall.restserver.endpoints.ep_sensor_trigger_report import EPSensorTriggerReport

from greenwall.restserver.endpoints.ep import EP

class SensorView(FlaskView):
    representations = {'application/json': output_json}
    inspect_args = False

    def __init__(self, web_gadget):

        self.web_gadget = web_gadget

        self.epSensorRegister = EPSensorRegister(web_gadget)
        self.epSensorAdd = EPSensorAdd(web_gadget)
        self.epSensorDataList = EPSensorDataList(web_gadget)
        self.epSensorDataAverageById = EPSensorDataAverageById(web_gadget)
        self.epSensorRegisteredList = EPSensorRegisteredList(web_gadget)
        self.epSensorTriggerReport = EPSensorTriggerReport(web_gadget)


    #
    # GET http://localhost:5000/sensor/
    #
    def index(self):
        return {}


# === POST /sensor/register ===

    #
    # Register Sensor Station with payload - called from station module
    #
    # curl  --header "Content-Type: application/json" --request POST --data '{"stationId": "5","configureUrl": "http://192.168.0.23:80/configure", "measureActualUrl": "http://192.168.0.23:80/all/actuall", "collectAverageUrl": "http://192.168.0.23:80/all/average" }' http://localhost:5000/sensor/register
    #
    # POST http://localhost:5000/sensor/register
    #      body: {
    #        "stationId":"5"
    #        "configureUrl": "http://192.168.0.23:80/configure",
    #        "measureActualUrl": "http://192.168.0.23:80/all/actual",
    #        "collectAverageUrl": "http://192.168.0.23:80/all/average",
    #        "dateString": "2022.11.05T01:01:01+01:00",
    #      }
    #
    #@route('/register', methods=['POST'])
    @route(EPSensorRegister.PATH_PAR_PAYLOAD, methods=[EPSensorRegister.METHOD])
    def registerSensorWithPayload(self):

        logging.debug("POST sensor/register node was called from the sensor station module")

        # WEB
        if request.form:
            json_data = request.form

        # CURL
        elif request.json:
            json_data = request.json

        else:
            return "Not valid request", EP.CODE_BAD_REQUEST

        out = self.epSensorRegister.executeByPayload(json_data)
        return out

# === POST /sensor/add ===

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


# === POST /sensor/data/list ===


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





# === GET /sensor/data/average/id ===

    #
    # Get the Average value of a Sensor Station module
    #
    # curl  --request GET http://localhost:5000/sensor/data/average/id/{id}
    #
    # GET http://localhost:5000/sensor/data/average/

    #@route('/configure/data/average/ip/{ip}', methods=['GET'])
    @route(EPSensorDataAverageById.PATH_PAR_URL, methods=[EPSensorDataAverageById.METHOD])
    def sensorDataAverageByIdWithParameter(self, id):

        out = self.epSensorDataAverageById.executeByParameters(id=id)

        return out

# === GET /sensor/registered/list ===

    #
    # Get the list of the registered Sensor Stations
    #
    # curl  --request GET http://localhost:5000/sensor/registered/list
    #
    # GET http://localhost:5000/sensor/registered/list

    #@route('/registered/list', methods=['GET'])
    @route(EPSensorRegisteredList.PATH_PAR_URL, methods=[EPSensorRegisteredList.METHOD])
    def sensorGetRegisteredListWithParameter(self):

        out = self.epSensorRegisteredList.executeByParameters()

        return out



    #@route('/trigger/report', methods=['POST'])
    @route(EPSensorTriggerReport.PATH_PAR_URL, methods=[EPSensorTriggerReport.METHOD])
    def sensorTriggerReport(self):

        out = self.epSensorTriggerReport.executeByParameters()

        return out
