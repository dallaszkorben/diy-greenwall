import json
from flask import Flask
from flask import jsonify
from flask import session
from flask_classful import FlaskView, route, request

#from wgadget.exceptions import InvalidAPIUsage
from exceptions.invalid_api_usage import InvalidAPIUsage

from wgadget.representations import output_json

from threading import Thread

from egadget.eg_light import EGLight

from config.config_exchange import getConfigExchange
from config.config_exchange import setConfigExchange
from config.config_egadget import getConfigEGadget

from wgadget.endpoints.ep_gradually_set_light import EPGraduallySetLight
from wgadget.endpoints.ep_gradually_increase_light import EPGraduallyIncreaseLight
from wgadget.endpoints.ep_gradually_schedule_set_light import EPGraduallyScheduleSetLight

# -----------------------------------
#
# POST Contorl the level of the light
#
# curl  --header "Content-Type: application/json" --request POST http://localhost:5000/gradually/set/actuatorId/1/value/10/inSeconds/3
# curl  --header "Content-Type: application/json" --request POST --data '{"actuatorId":1,"value":10,"inSeconds":3}' http://localhost:5000/gradually/set
#
# curl  --header "Content-Type: application/json" --request POST http://localhost:5000/gradually/increase/actuatorId/1/stepValue/-10/inSeconds/3
# curl  --header "Content-Type: application/json" --request POST --data '{"actuatorId":1,"stepValue":-10,"inSeconds":3}' http://localhost:5000/gradually/increase
#
# curl  --header "Content-Type: application/json" --request POST http://localhost:5000/gradually/schedule/set/actuatorId/1/value/100/inSeconds/3/atDateTime/2021-02-14T21:15:00
# curl  --header "Content-Type: application/json" --request POST --data '{"actuatorId":1,"value":10,"inSeconds":3,"atDateTime":"2021-02-14T21:15:00"}' http://localhost:5000/gradually/schedule/set
#
# -----------------------------------
#
# GET http://localhost:5000/gradually
class GraduallyView(FlaskView):
    representations = {'application/json': output_json}
    inspect_args = False

    def __init__(self, web_gadget):
        self.web_gadget = web_gadget

        self.epGraduallySetLight = EPGraduallySetLight(web_gadget)
        self.epGraduallyIncreaseLight = EPGraduallyIncreaseLight(web_gadget)
        self.epGraduallyScheduleSetLight = EPGraduallyScheduleSetLight(web_gadget)

    #
    # GET http://localhost:5000/set/
    #
    def index(self):
        return {}

# ===

    #
    # Set the light value gradually with payload
    #
    # curl  --header "Content-Type: application/json" --request POST --data '{"actuatorId":1,"value":10,"inSeconds":3}' http://localhost:5000/gradually/set
    #
    # POST http://localhost:5000/gradually/set
    #      body: {
    #                'actuatorId': "1',
    #                'value: '13'
    #                'inSeconds: '3'
    #           }
    #
    @route("/set",  methods=['POST'] )
    def setWithPayload(self):

        # WEB
        if request.form:
            json_data = request.form

        # CURL
        elif request.json:
            json_data = request.json

        else:
            return {}

        self.epGraduallySetLight.executeByPayload(json_data)

        return {'status': 'OK'}

    #
    # Set the light value gradually
    #
    # curl  --header "Content-Type: application/json" --request POST http://localhost:5000/gradually/set/actuatorId/1/value/10/inSeconds/3
    #
    # POST http://localhost:5000/gradually/set/actuatorId/1/value/10/inSeconds/3
    #
    #@route('/set/actuatorId/<actuatorId>/value/<value>/inSeconds/<inSeconds>', methods=['POST'])
    @route(EPGraduallySetLight.URL_ROUTE_PAR_URL, methods=[EPGraduallySetLight.METHOD])
    def set(self, actuatorId, value, inSeconds):

        self.epGraduallySetLight.executeByParameters(actuatorId=actuatorId, value=value, inSeconds=inSeconds)

        return {'status': 'OK'}

# ===

    #
    # Increase the light value gradually with payload
    #
    # curl  --header "Content-Type: application/json" --request POST --data '{"actuatorId":1,"stepValue":-10,"inSeconds":3}' http://localhost:5000/gradually/increase
    #
    #      body: {
    #                'actuatorId': "1',
    #                'stepValue: '-10'
    #                'inSeconds: '3'
    #           }
    #
    #@route("/increase",  methods=['POST'] )
    @route(EPGraduallyIncreaseLight.URL_ROUTE_PAR_PAYLOAD,  methods=[EPGraduallyIncreaseLight.METHOD] )
    def increaseWithPayload(self):

        # WEB
        if request.form:
            json_data = request.form

        # CURL
        elif request.json:
            json_data = request.json

        else:
            return {}

        self.epGraduallyIncreaseLight.executeByPayload(json_data)

        return {'status': 'OK'}

    #
    # Increase the light value gradually
    #
    # curl  --header "Content-Type: application/json" --request POST http://localhost:5000/gradually/increase/actuatorId/1/stepValue/-10/inSeconds/3
    #
    #
    #@route('/increase/actuatorId/<actuatorId>/stepValue/<stepValue>/inSeconds/<inSeconds>', methods=['POST'])
    @route(EPGraduallyIncreaseLight.URL_ROUTE_PAR_URL,  methods=[EPGraduallyIncreaseLight.METHOD] )
    def increase(self, actuatorId, stepValue, inSeconds):

        self.epGraduallyIncreaseLight.executeByParameters(actuatorId=actuatorId, stepValue=stepValue, inSeconds=inSeconds)

        return {'status': 'OK'}

# ===



    #
    # Set the light value gradually in a scheduled time
    #
    # curl  --header "Content-Type: application/json" --request POST --data '{"actuatorId":1,"value":10,"inSeconds":3,"atDateTime":"2021-02-14T21:15:00"}' http://localhost:5000/gradually/schedule/set
    #
    # POST http://localhost:5000/gradually/schedule/set
    #      body: {
    #                'actuatorId': 1,
    #                'value: 13
    #                'inSeconds: 3,
    #                "atDateTime":"2021-02-14T21:15:00"
    #           }
    #
    #@route("/schedule/set",  methods=['POST'] )
    @route(EPGraduallyScheduleSetLight.URL_ROUTE_PAR_PAYLOAD,  methods=[EPGraduallyScheduleSetLight.METHOD] )
    def scheduleSetWithPayload(self):

        # WEB
        if request.form:
            json_data = request.form

        # CURL
        elif request.json:
            json_data = request.json

        else:
            return {}

        self.epGraduallyScheduleSetLight.executeByPayload(json_data)

        return {'status': 'OK'}


    #
    # Set the light value gradually in a scheduled time
    #
    # curl  --header "Content-Type: application/json" --request POST http://localhost:5000/gradually/schedule/set/actuatorId/1/value/100/inSeconds/3/atDateTime/2021-02-14T21:15:00
    #
    # POST http://localhost:5000/gradually/schedule/set/actuatorId/1/value/100/inSeconds/3/atDateTime/2021-02-14T21:15:00+01:00
    #
    #@route('schedule/set/actuatorId/<actuatorId>/value/<value>/inSeconds/<inSeconds>/atDateTime/<atDateTime>', methods=['POST'])
    @route(EPGraduallyScheduleSetLight.URL_ROUTE_PAR_URL,  methods=[EPGraduallyScheduleSetLight.METHOD] )
    def scheduleSet(self, actuatorId, value, inSeconds, atDateTime):

        self.epGraduallyScheduleSetLight.executeByParameters(actuatorId=actuatorId, value=value, inSeconds=inSeconds, atDateTime=atDateTime)

        return {'status': 'OK'}


