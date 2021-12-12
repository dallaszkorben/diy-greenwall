import machine, time
from machine import Pin
import math

# "zero-level": 76,
# "quadratic-a": -2.7354525,
# "quadratic-b": 0.262834668,
# "quadratic-c": 0.000210552445

class SensorLevel():

    MAX_DISTANCE_IN_M = 1.0		# 1 m max distance

    def __init__(self, triggerGpio, echoGpio, sampleNumber, a=None, b=None, c=None):

        self.trigger = Pin(triggerGpio, mode=Pin.OUT, pull=None)
        self.echo = Pin(echoGpio, mode=Pin.IN, pull=None)
        self.echo_timeout_us=int(1000000*SensorLevel.MAX_DISTANCE_IN_M/347.125) # calculate time for 1m max distance
        self.sampleNumber = sampleNumber

        self.a = a
        self.b = b
        self.c = c

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

        return (self.a + self.b * pulse + self.c * pulse * pulse, pulse)

    def getDistanceMeanInMm(self):

        distanceList = [self.getDistanceInMm()[0] for x in range(self.sampleNumber)]

        # Number of observations
        n = len(distanceList)

        # Mean of the data
        mean = sum(distanceList) / n

        # Square deviations
        deviations = [(x - mean) ** 2 for x in distanceList]

        # Variance
        variance = math.sqrt( sum(deviations) / n )

        return (mean, variance)

