import time
import config
import gc
import machine
from machine import Timer
import utime

import ujson

gc.enable()
gc.collect()

# ###########################################################
#
# Parameter Load
#
# ###########################################################

#
# central-ap
#
ip=config.getValue('central-ap', 'webserver-ip')
path_level_add=config.getValue('central-ap', 'webserver-path-level-add')
path_info_timestamp=config.getValue('central-ap', 'webserver-path-info-timestamp')

#
# level-sta
#
stationId=config.getValue('level-sta', 'station-id')
reportIntervalSec=config.getValue('level-sta', 'report-interval-sec')
resetHours=config.getValue('level-sta', 'reset-hours')
#pinAnalog=config.getValue('level-sta', 'analog-pin')

#
# sensor-level
#
sensorLevelPackageName=config.getValue('sensor-level', 'package-name')
pinTrigger=config.getValue('sensor-level', 'trigger-pin')
pinEcho=config.getValue('sensor-level', 'echo-pin')
sampleNumber=config.getValue('sensor-level', 'sample-number')
maximumVariance=config.getValue('sensor-level', 'maximum-variance')

#
# sensor-temperature-humidity
#
sensorTempHumPackageName=config.getValue('sensor-temp-hum', 'package-name')
dataGpio=config.getValue('sensor-temp-hum', 'data-gpio')

# ###########################################################

SensorLevel=__import__(sensorLevelPackageName).SensorLevel
SensorTempHum=__import__(sensorTempHumPackageName).SensorTempHum

print()
gc.collect()

class LevelCalibration():

    def calibrate():

        while True:
            gc.collect()

            a=0
            b=1
            c=0
            wls=SensorLevel(pinTrigger, pinEcho, sampleNumber, a=a, b=b, c=c)

            pulse = wls.getDistanceMeanInMm()

            print("\r {0}        ".format(pulse),  end="")

            time.sleep(0.5)

    def check():

        while True:
            gc.collect()

            a = 49.370704
            b = 0.07206394
            c = -0.00031533548

            wls=SensorLevel(pinTrigger, pinEcho, sampleNumber, a=a, b=b, c=c)

#            pulse = wls.getDistanceMeanInMm()
            level = wls.getDistanceMeanInMm()

            print("\r {0}        ".format(level),  end="")

            time.sleep(0.5)
