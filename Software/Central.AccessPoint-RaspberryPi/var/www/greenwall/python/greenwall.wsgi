#! /var/www/greenwall/python/env/bin/python

import sys,os

print("The greenwall app started: %s" % (__file__))

sys.path.insert(0, os.path.realpath(os.path.dirname(__file__)))

from greenwall.restserver.ws_greenwall import app as application
