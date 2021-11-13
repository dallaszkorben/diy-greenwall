#! /usr/bin/python3

from webserver.ws_greenwall import app as application

if __name__ == "__main__":

    try:

        application.run(host= '0.0.0.0', debug=True)
#        application.run(host= '0.0.0.0', debug=False, threaded=True)
#        application.run(host= '0.0.0.0', debug=False, threaded=False)


    finally:
        application.unconfigure()
