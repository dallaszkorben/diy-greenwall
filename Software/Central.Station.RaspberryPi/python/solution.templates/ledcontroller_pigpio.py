#! /usr/bin/python3

import pigpio
from time import sleep
import math

PIN_PWM = 18 #12 #18
PIN_UP = 23 #16 #23
PIN_DOWN = 24 #18 #24

PWM_FREQ = 800

MIN_DUTY_CYCLE = 0
MAX_DUTY_CYCLE = 1000000

SLEEP = 0.1

POTMETER_MIN = 0.0
POTMETER_MAX = 100.0
POTMETER_STEP = 1.0

pi_pwm = pigpio.pi()

pi_pwm.set_mode(PIN_PWM, pigpio.OUTPUT)
pi_pwm.set_mode(PIN_UP, pigpio.INPUT)
pi_pwm.set_mode(PIN_DOWN, pigpio.INPUT)

# 0-100
potmeterValue = MIN_DUTY_CYCLE
#pi_pwm.start(potmeterValue)
#pi_pwm.set_servo_pulsewidth(PIN_PWM, 500)
#pi_pwm.start(0)



while True:
#        up_value = GPIO.input(PIN_UP)
#        down_value = GPIO.input(PIN_DOWN)

        up_value = pi_pwm.read(PIN_UP)
        down_value = pi_pwm.read(PIN_DOWN)

        change = False

#        print(up_value, down_value)

        if up_value and down_value:
            potmeterValue = 0
            change = True 

        elif up_value and potmeterValue < POTMETER_MAX:
            potmeterValue += 1
            change = True


        elif down_value and potmeterValue > POTMETER_MIN:
            potmeterValue -= 1
            change = True

        if change:

            #print(potmeterValue)

            # 0 ,,, 1
            normalizedValue = potmeterValue / POTMETER_MAX

            POWER = 80

            # 1 ... POWER -> 0 ,,, (POWER-1)
            expValue = math.pow(POWER, normalizedValue) - 1

            # 0 ... MAX_DUTY_CYCLE
            fadeValue = (int)(MAX_DUTY_CYCLE * expValue / (POWER - 1))

            # Change the Duty Cycle
            pi_pwm.hardware_PWM(PIN_PWM, PWM_FREQ, fadeValue)

            print(potmeterValue, expValue, fadeValue)

        sleep(SLEEP)









