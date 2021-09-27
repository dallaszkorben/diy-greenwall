import config
from machine import Pin, PWM

class LedControl():

    MAX_DUTY = 1023

    INVERSE = config.getValue('level-sta', 'led-status-inverse')

    STATUS_BEFORE_SEND_POST = {
        "freq": 1000,
        "duty": (MAX_DUTY-1023) if INVERSE else 1023
    }
    STATUS_FAILED_SEND_POST = {
        "freq": 10,
        "duty": (MAX_DUTY-500) if INVERSE else 500
    }
    STATUS_PASSED_SEND_POST = {
        "freq": 1,
        "duty": (MAX_DUTY-30) if INVERSE else 30
    }
    STATUS_FAILED_CONNECTION = {
        "freq": 1000,
        "duty": (MAX_DUTY-20) if INVERSE else 20
    }
    STATUS_BEFORE_CONNECTION = {
        "freq": 1,
        "duty": (MAX_DUTY-500) if INVERSE else 500
    }

    def __init__(self):
        self.pinLedStatus=config.getValue('level-sta', 'led-status-pin')

    def setBeforeSendPost(self):
        led = PWM(Pin(self.pinLedStatus), freq=LedControl.STATUS_BEFORE_SEND_POST['freq'], duty=LedControl.STATUS_BEFORE_SEND_POST['duty'])

    def setPassedSendPost(self):
        led = PWM(Pin(self.pinLedStatus), freq=LedControl.STATUS_PASSED_SEND_POST['freq'], duty=LedControl.STATUS_PASSED_SEND_POST['duty'])

    def setFailedSendPost(self):
        led = PWM(Pin(self.pinLedStatus), freq=LedControl.STATUS_FAILED_SEND_POST['freq'], duty=LedControl.STATUS_FAILED_SEND_POST['duty'])

    def setFailedConnection(self):
        led = PWM(Pin(self.pinLedStatus), freq=LedControl.STATUS_FAILED_CONNECTION['freq'], duty=LedControl.STATUS_FAILED_CONNECTION['duty'])

    def setBeforeConnection(self):
        led = PWM(Pin(self.pinLedStatus), freq=LedControl.STATUS_BEFORE_CONNECTION['freq'], duty=LedControl.STATUS_BEFORE_CONNECTION['duty'])
