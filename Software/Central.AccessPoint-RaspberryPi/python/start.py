#! /usr/bin/python3

from restserver.ws_greenwall import WSGreenWall

if __name__ == "__main__":

    application = WSGreenWall(__name__)

    try:

        #disable the reloader using use_reloader=False, otherwise the Flask ran again
        application.run(host= '0.0.0.0', debug=True, use_reloader=False, threaded=True)
#        application.run(host= '0.0.0.0', debug=False, threaded=False)

    finally:

        application.unconfigure()
