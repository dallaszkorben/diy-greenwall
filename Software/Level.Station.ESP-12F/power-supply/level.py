#from ultrasonic_sensor import UltrasonicSensor
from water_level_sensor import WaterLevelSensor
from wifi_level import WifiLevel
import time
import config
import gc

gc.enable()

# ###########################################################
#
# Parameter Load
#
# ###########################################################
ip=config.getValue('central-ap', 'webserver-ip')
path=config.getValue('central-ap', 'webserver-path-level-report')

pinAnalog=config.getValue('level-sta', 'analog-pin')
#pinTrigger=config.getValue('level-sta', 'trigger-pin')
#pinEcho=config.getValue('level-sta', 'echo-pin')
reportIntervalSec=config.getValue('level-sta', 'report-interval-sec')

zeroLevel=config.getValue('ultrasonic-sensor', 'zero-level')
m=config.getValue('ultrasonic-sensor', 'linear-m')
b=config.getValue('ultrasonic-sensor', 'linear-b')
sampleNumber=config.getValue('ultrasonic-sensor', 'sample-number')
maximumVariance=config.getValue('ultrasonic-sensor', 'maximum-variance')
# ###########################################################

wl=WifiLevel()
#wl.connectToAp()

#
# Depending on what kind of sensor is used
#
#wls=UltrasonicSensor(pinTrigger, pinEcho, zeroLevel, m, b, sampleNumber)
wls=WaterLevelSensor(pinAnalog, sampleNumber, m, b)

print()

gc.collect()

while True:

#    print("Waiting for the next sample, ", end="")
    minLevel=(None, None)
    counter = 0
    while True:
#    dist = us.getDistanceMeanInMm()

        level = wls.getLevelMeanInMm()
        gc.collect()

        phase = counter % 4
        print("-\r" if phase == 0 else "\\\r" if phase == 1 else "|\r" if phase == 2 else "/\r", end="")

        # save if it is lower than
        if minLevel[1] == None or minLevel[1] > level[1]:
            minLevel = (level[0], level[1])

        if minLevel[1] < maximumVariance:
            break

        # for long time there was NO expectable variance
        if counter > 500:
            break

        counter = counter + 1
        time.sleep_ms(10)

    result = wl.sendPost(address=ip, path=path, data='{"levelId": 5, "value":' + str(int(minLevel[0])) + ', "variance": ' + '{:.3f}'.format(minLevel[1]) + '}')
    gc.collect()

    # Unsuccessful send
    if not result:
        time.sleep(10)
        continue

    time.sleep(reportIntervalSec)

