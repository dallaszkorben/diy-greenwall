import ujson
import re
import gc
import math
from time import sleep
from machine import Pin, PWM


class LampControl:

    FREQ = 5000
    MAX_PERC = 100.0
    MAX_DUTY = 1024
    STEP_SEC = 0.1

    def __init__(self, lampGpio):
        gc.enable()

        dutyCycle = 0

        print("lampGpio: {0}".format(lampGpio))
        self.led = PWM(Pin(lampGpio), LampControl.FREQ)

        gc.collect()

    def on(self, lengthInSec):

        steps = lengthInSec / LampControl.STEP_SEC
        dutyStep = LampControl.MAX_PERC / steps

        dutyCycle = 0
        while dutyCycle <= (LampControl.MAX_PERC + dutyStep):

            printMessage = "Process duty: {0}     ".format(int(self.getValue(dutyCycle)))
            print( printMessage, end="\b"*len(printMessage))

            self.led.duty(int(self.getValue(dutyCycle)))

            gc.collect()

            sleep(LampControl.STEP_SEC)

            dutyCycle += dutyStep

        print()

    def off(self, lengthInSec):

        steps = lengthInSec / LampControl.STEP_SEC
        dutyStep = LampControl.MAX_PERC / steps

        dutyCycle = LampControl.MAX_PERC
        while dutyCycle >= -dutyStep:

            printMessage = "Process duty: {0}     ".format(int(self.getValue(dutyCycle)))
            print( printMessage, end="\b"*len(printMessage))

            self.led.duty(int(self.getValue(dutyCycle)))

            gc.collect()

            sleep(LampControl.STEP_SEC)

            dutyCycle -= dutyStep

        print()

    def getValue(self, perc):
        return math.pow(self.min(100, self.max(0, perc)), 1.50493781686)

    def max(self, value1, value2):
        if value1 > value2:
            return value1
        else:
            return value2

    def min(self, value1, value2):
        if value1 < value2:
            return value1
        else:
            return value2
