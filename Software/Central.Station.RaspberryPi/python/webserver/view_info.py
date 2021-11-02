import json

from flask import Flask
from flask import jsonify
from flask import session
from flask_classful import FlaskView, route, request

from webserver.representations import output_json

from threading import Thread

from exceptions.invalid_api_usage import InvalidAPIUsage

from webserver.endpoints.ep_info_functions import EPInfoFunctions

# -----------------------------------
#
# GET info
#
# curl  --header "Content-Type: application/json" --request GET http://localhost:5000/info/request
# -----------------------------------
#
# GET http://localhost:5000/info
class InfoView(FlaskView):
    representations = {'application/json': output_json}
    inspect_args = False

    def __init__(self, web_gadget):

        self.web_gadget = web_gadget

        self.epInfoFunctions = EPInfoFunctions(web_gadget)

    #
    # GET http://localhost:5000/info/
    #
    def index(self):
        return {}

    #
    # Get the info about possible requests
    #
    # curl  --header "Content-Type: application/json" --request GET http://localhost:5000/info/functions
    #
    # GET http://localhost:5000/info/functions
    #
    #@route('/functions, methods=['GET'])
    @route(EPInfoFunctions.PATH_PAR_URL, methods=[EPInfoFunctions.METHOD])
    def getInfoFunctions(self):

        resp = self.epInfoFunctions.executeByParameters()
        result = resp 

        return result
