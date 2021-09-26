import config
from machine import Pin, PWM


class LedControl():

    STATUS_NONE = -1
    STATUS_IS_AP = 0
    STATUS_IS_WEB = 1
    STATUS_NO_AP = 2
    STATUS_NO_WEB = 3

    def __init__(self):
        self.status=LedControl.STATUS_NONE
        self.pinLedRed=config.getValue('level-sta', 'pin-led-red')
        self.pinLedGreen=config.getValue('level-sta', 'pin-led-green')

    def isWeb(self):
        if not self.status == LedControl.STATUS_IS_WEB:
            ledRed = PWM(Pin(self.pinLedRed), freq=1, duty=0)
            ledGreen = PWM(Pin(self.pinLedGreen), freq=1, duty=50)
            self.status = LedControl.STATUS_IS_WEB

    def isAp(self):
        if not self.status == LedControl.STATUS_IS_AP:
            ledRed = PWM(Pin(self.pinLedRed), freq=1, duty=0)
            ledGreen = PWM(Pin(self.pinLedGreen), freq=1, duty=0)
            self.status = LedControl.STATUS_IS_AP

    def noAp(self):
        if not self.status == LedControl.STATUS_NO_AP:
            ledRed = PWM(Pin(self.pinLedRed), freq=1000, duty=1000)
            ledGreen = PWM(Pin(self.pinLedGreen), freq=1, duty=0)
            self.status = LedControl.STATUS_NO_AP

    def noWeb(self):
        if not self.status == LedControl.STATUS_NO_WEB:
            ledRed = PWM(Pin(self.pinLedRed), freq=1, duty=500)
            ledGreen = PWM(Pin(self.pinLedGreen), freq=1, duty=0)
            self.status = LedControl.STATUS_NO_WEB

