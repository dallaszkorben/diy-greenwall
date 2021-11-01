#! /usr/bin/python3

#from wgadget.wg_light import WGLight

from wgadget.wg_greenwall import app as application

if __name__ == "__main__":

#    wgLight = WGLight(__name__)

    try:
        application.run(host= '0.0.0.0', debug=False)
#        wgLight.run()

    finally:
        application.unconfigure()
