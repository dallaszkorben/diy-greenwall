import machine, time
#from machine import Pin
from machine import Pin, ADC
import math

# "zero-level": 59,
# "linear-m": 0.11,
# "linear-b": -35,
class SensorLevel():

    def __init__(self, analogGpio, sampleNumber, m, b):

        self.analog = ADC(analogGpio)
        self.sampleNumber = sampleNumber

        self.m = m
        self.b = b

    def getDistanceInMm(self):

        level = self.analog.read()

        return (int(self.m * level + self.b), level)
        #return (int(level), level)

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


    def getLevelMeanInMm(self):
        dist = self.getDistanceMeanInMm()
        return (dist[0], dist[1])