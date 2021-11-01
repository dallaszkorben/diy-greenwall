#! /usr/bin/python3

import RPi.GPIO as GPIO
from time import sleep
import math

PIN_PWM = 18
PIN_UP = 23
PIN_DOWN = 24

PWM_FREQ = 100

MIN_DUTY_CYCLE = 0
MAX_DUTY_CYCLE = 100

SLEEP = 0.3

POTMETER_MIN = 0.0
POTMETER_MAX = 100.0
POTMETER_STEP = 1.0

#GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)

GPIO.setup(PIN_PWM, GPIO.OUT)
GPIO.setup(PIN_UP, GPIO.IN)
GPIO.setup(PIN_DOWN, GPIO.IN)

pi_pwm = GPIO.PWM(PIN_PWM, PWM_FREQ)

# 0-100
potmeterValue = MIN_DUTY_CYCLE
#pi_pwm.start(potmeterValue)
pi_pwm.start(0)

try:

    while True:
        up_value = GPIO.input(PIN_UP)
        down_value = GPIO.input(PIN_DOWN)
        change = False

#        print(up_value, down_value)

        if up_value and potmeterValue < POTMETER_MAX:
            potmeterValue += 1
            change = True


        elif down_value and potmeterValue > POTMETER_MIN:
            potmeterValue -= 1
            change = True

        if change:

            # 1-2
            normalizedValue = potmeterValue / POTMETER_MAX + 1.0

            # 10-100 -> 0-90
            expValue = math.pow(10, normalizedValue) - 10

            # 0-MAX_DUTY_CYCLE
            fadeValue = expValue * MAX_DUTY_CYCLE / 90

            # Change the Duty Cycle
            pi_pwm.ChangeDutyCycle(fadeValue)

            print(potmeterValue, fadeValue)

        sleep(SLEEP)

except:
    print('hello')

finally:
    GPIO.cleanup()