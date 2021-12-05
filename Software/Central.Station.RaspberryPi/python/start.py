#! /usr/bin/python3

#from restserver.ws_greenwall import app as application

from restserver.ws_greenwall import WSGreenWall

if __name__ == "__main__":

    application = WSGreenWall(__name__)

    try:

        application.run(host= '0.0.0.0', debug=True)

#        application.run(host= '0.0.0.0', debug=True)
#        application.run(host= '0.0.0.0', debug=False, threaded=True)
#        application.run(host= '0.0.0.0', debug=False, threaded=False)

    finally:
        application.unconfigure()
