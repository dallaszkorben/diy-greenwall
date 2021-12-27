#!/usr/bin/python3

import sys
sys.path.insert(0,"/var/www/greenwall/python")

#try:
#from wgadget.wg_light import app as application

from webserver.ws_greenwall import app as application

#finally:
#    application.unconfigure()
