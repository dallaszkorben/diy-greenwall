from wifi_control import WifiControl
from web_server import WebServer
from lamp_control import LampControl
import time
import config
import gc
import machine
from machine import Timer
import utime

import ujson


gc.enable()

# ###########################################################
#
# Parameter Load
#
# ###########################################################

#
# central-ap
#
ip=config.getValue('central-ap', 'webserver-ip')
path_info_timestamp=config.getValue('central-ap', 'webserver-path-info-timestamp')
path_pwm_register=config.getValue('central-ap', 'webserver-path-pwm-register')
path_swithch_register=config.getValue('central-ap', 'webserver-path-switch-register')

#
# control-sta
#
lampId=config.getValue('control-sta', 'lamp-id')
pwmGpio=config.getValue('control-sta', 'pwm-gpio')
onOffGpio=config.getValue('control-sta', 'on-off-gpio')
ledStatusGpio=config.getValue('control-sta', 'led-status-gpio')
ledStatusInverse=config.getValue('control-sta', 'led-status-inverse')
reportIntervalSec=config.getValue('control-sta', 'report-interval-sec')
resetHours=config.getValue('control-sta', 'reset-hours')

# ###########################################################

def hello():
    pass

class ControlStation():

    def __init__(self):

        gc.collect()

        print()

        # Have to reset the chip, because for some reson, the pythin got frozen after some hours
        #resetMiliseconds = resetHours * 60 * 60 * 1000 # [ms]
        #timer=Timer(-1)
        #timer.init(period=resetMiliseconds, mode=Timer.ONE_SHOT, callback=lambda t:machine.reset())

        self.lc=LampControl(pwmGpio)
        self.wc=WifiControl()

        healthTimer = Timer(0)
        healthTimer.init(period=30000, mode=Timer.PERIODIC, callback=lambda t:self.checkHealth())
        #healthTimer.init(period=60000, mode=Timer.PERIODIC, callback=lambda t:self.wc.registerLamp())
        #healthTimer.init(period=60000, mode=Timer.PERIODIC, callback=hello)

        gc.collect()

    def checkHealth(self):
        gc.collect()

#        result = self.wc.registerLamp()
#        if not result['success']:
#            print("!!! Reset Station because it can not register lamp !!!")
#            machine.reset()

        gc.collect()
        return

    def start(self):
        self.ws=WebServer(self.lc)

cs = ControlStation()
cs.start()

