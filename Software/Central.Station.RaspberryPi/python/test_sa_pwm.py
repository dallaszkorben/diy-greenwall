#! /usr/bin/python3

from time import sleep
import logging
from senact.sa_pwm import SAPwm

#test
if __name__ == "__main__":

    ID = 1

    PWM_PIN = 18
    PWM_FREQ = 800

    DIR_UP = 1
    DIR_DOWN = -1

    saPwm = SAPwm(ID, PWM_PIN, PWM_FREQ)
    saPwm.configure()

    def triggerValue(value):
        print(value)
        saPwm.setPwmByValue(value)

    try:

        value = 0
        direction = DIR_UP
        while True:

            triggerValue(value)
            value += direction
            if value >= 100:
                direction = DIR_DOWN
            elif value <= 0:
                direction = DIR_UP
            sleep(0.1)

    finally:
        saPwm.unconfigure()



