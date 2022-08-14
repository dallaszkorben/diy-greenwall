#! /var/www/greenwall/python/env/bin/python

import sys,os
sys.path.insert(0, os.path.realpath(os.path.dirname(__file__)))
from greenwall.restserver.ws_greenwall import app as application

if __name__ == "__main__":


    try:
        #disable the reloader using use_reloader=False, otherwise the Flask ran again
        application.run(host= '0.0.0.0', debug=True, use_reloader=False, threaded=True)

    finally:
        application.unconfigure()





