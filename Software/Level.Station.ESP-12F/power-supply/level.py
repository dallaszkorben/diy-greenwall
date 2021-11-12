from ultrasonic_sensor import UltrasonicSensor
#from water_level_sensor import WaterLevelSensor
from wifi_level import WifiLevel
import time
import config
import gc
import machine
from machine import Timer



gc.enable()

# ###########################################################
#
# Parameter Load
#
# ###########################################################
ip=config.getValue('central-ap', 'webserver-ip')
path=config.getValue('central-ap', 'webserver-path-level-report')

levelId=config.getValue('level-sta', 'level-id')
reportIntervalSec=config.getValue('level-sta', 'report-interval-sec')
resetHours=config.getValue('level-sta', 'reset-hours')

#pinAnalog=config.getValue('level-sta', 'analog-pin')
pinTrigger=config.getValue('level-sta', 'trigger-pin')
pinEcho=config.getValue('level-sta', 'echo-pin')

zeroLevel=config.getValue('level-sensor', 'zero-level')
m=config.getValue('level-sensor', 'linear-m')
b=config.getValue('level-sensor', 'linear-b')
sampleNumber=config.getValue('level-sensor', 'sample-number')
maximumVariance=config.getValue('level-sensor', 'maximum-variance')
# ###########################################################

wl=WifiLevel()
#wl.connectToAp()

#
# Depending on what kind of sensor is used
#
wls=UltrasonicSensor(pinTrigger, pinEcho, zeroLevel, m, b, sampleNumber)
#wls=WaterLevelSensor(pinAnalog, sampleNumber, m, b)

print()

gc.collect()

# Have to reset the chip, because for some reson, the pythin got frozen after some hours
resetMiliseconds = resetHours * 60 * 60 * 1000 # [ms]
timer=Timer(-1)
timer.init(period=resetMiliseconds, mode=Timer.ONE_SHOT, callback=lambda t:machine.reset())

while True:

    minLevel=(None, None)
    counter = 0

    # Reading water level
    while True:

        level = wls.getLevelMeanInMm()

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
        time.sleep_ms(1)

    result = wl.sendPost(address=ip, path=path, data='{"levelId": ' + levelId + ', "value":' + str(int(minLevel[0])) + ', "variance": ' + '{:.3f}'.format(minLevel[1]) + '}')
    gc.collect()

    # Unsuccessful send
    if not result:
        time.sleep(1)
        continue

    time.sleep(reportIntervalSec)

