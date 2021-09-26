import machine, time
from machine import Pin
import math
class UltrasonicSensor():

    SAMPLE_NUMBER = 100			#Number of samples for mean value
    MAX_DISTANCE_IN_M = 1.0		# 1 m max distance
    CONVERTER_TO_DISTANCE = 0.173563

    def __init__(self, triggerGpio, echoGpio):

        self.trigger = Pin(triggerGpio, mode=Pin.OUT, pull=None)
        self.echo = Pin(echoGpio, mode=Pin.IN, pull=None)
        self.echo_timeout_us=int(1000000*UltrasonicSensor.MAX_DISTANCE_IN_M/347.125) # calculate time for 1m max distance

    def getPulse(self):
       self.trigger.value(0) 
       time.sleep_us(5)
       self.trigger.value(1)
       time.sleep_us(20)
       self.trigger.value(0)

       try:
          pulse_time = machine.time_pulse_us(self.echo, 1, self.echo_timeout_us)
          return pulse_time
       except OSError as ex:
          print("exception: ", ex)
          if ex.args[0] == 110: 
             raise OSError('Out of range')
             raise ex

    def getDistanceInMm(self):
        time.sleep_us(2000)
        pulse = self.getPulse()
        return (int(UltrasonicSensor.CONVERTER_TO_DISTANCE * pulse), pulse)

    def getDistanceMeanInMm(self):

        distanceList = [self.getDistanceInMm()[0] for x in range(UltrasonicSensor.SAMPLE_NUMBER)]

        # Number of observations
        n = len(distanceList)

        # Mean of the data
        mean = sum(distanceList) / n

        # Square deviations
        deviations = [(x - mean) ** 2 for x in distanceList]

        # Variance
        variance = math.sqrt( sum(deviations) / n )

        return (mean, variance)