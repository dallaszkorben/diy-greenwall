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
path_register_pwm=config.getValue('central-ap', 'webserver-path-register-pwm')
path_register_on_off=config.getValue('central-ap', 'webserver-path-register-on-off')

#
# control-sta
#
stationId=config.getValue('control-sta', 'station-id')
pwmGpio=config.getValue('control-sta', 'pwm-gpio')
onOffGpio=config.getValue('control-sta', 'on-off-gpio')
ledStatusGpio=config.getValue('control-sta', 'led-status-gpio')
ledStatusInverse=config.getValue('control-sta', 'led-status-inverse')
reportIntervalSec=config.getValue('control-sta', 'report-interval-sec')
resetHours=config.getValue('control-sta', 'reset-hours')


# ###########################################################

print()

# Have to reset the chip, because for some reson, the pythin got frozen after some hours
resetMiliseconds = resetHours * 60 * 60 * 1000 # [ms]
timer=Timer(-1)
#timer.init(period=resetMiliseconds, mode=Timer.ONE_SHOT, callback=lambda t:machine.reset())

gc.collect()

wc=WifiControl()
lc=LampControl(pwmGpio)
ws=WebServer(lc)

