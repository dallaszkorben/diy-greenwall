import config
from machine import Pin, PWM

def getOffsetDateString(date):
    return "{0:04d}-{1:02d}-{2:02d}T{3:02d}:{4:02d}:{5:02d}".format(date[0], date[1], date[2], date[3], date[4], date[5] )

class LedControl():

    MAX_DUTY = 1023

    INVERSE = config.getValue('control-sta', 'led-status-inverse')

    STATUS_BEFORE_CONNECTION = {
        "freq": 15,
        "duty": (MAX_DUTY-50) if INVERSE else 50
    }

    STATUS_PASSED_CONNECTION = {
        "freq": 1,
        "duty": (MAX_DUTY-100) if INVERSE else 100
    }

    STATUS_FAILED_CONNECTION = {
        "freq": 1,
        "duty": (MAX_DUTY-500) if INVERSE else 800
    }

    STATUS_BEFORE_SEND_REST = {
        "freq": 25,
        "duty": (MAX_DUTY-200) if INVERSE else 50
    }

    STATUS_PASSED_SEND_REST = {
        "freq": 1,
        "duty": (MAX_DUTY-20) if INVERSE else 20
    }

    STATUS_FAILED_SEND_REST = {
        "freq": 1,
        "duty": (MAX_DUTY-500) if INVERSE else 500
    }

    def __init__(self):
        self.pinLedStatus=config.getValue('control-sta', 'led-status-gpio')

    def setBeforeConnection(self):
        led = PWM(Pin(self.pinLedStatus), freq=LedControl.STATUS_BEFORE_CONNECTION['freq'], duty=LedControl.STATUS_BEFORE_CONNECTION['duty'])

    def setPassedConnection(self):
        led = PWM(Pin(self.pinLedStatus), freq=LedControl.STATUS_PASSED_CONNECTION['freq'], duty=LedControl.STATUS_PASSED_CONNECTION['duty'])

    def setFailedConnection(self):
        led = PWM(Pin(self.pinLedStatus), freq=LedControl.STATUS_FAILED_CONNECTION['freq'], duty=LedControl.STATUS_FAILED_CONNECTION['duty'])

    def setBeforeSendRest(self):
        led = PWM(Pin(self.pinLedStatus), freq=LedControl.STATUS_BEFORE_SEND_REST['freq'], duty=LedControl.STATUS_BEFORE_SEND_REST['duty'])

    def setPassedSendRest(self):
        led = PWM(Pin(self.pinLedStatus), freq=LedControl.STATUS_PASSED_SEND_REST['freq'], duty=LedControl.STATUS_PASSED_SEND_REST['duty'])

    def setFailedSendRest(self):
        led = PWM(Pin(self.pinLedStatus), freq=LedControl.STATUS_FAILED_SEND_REST['freq'], duty=LedControl.STATUS_FAILED_SEND_REST['duty'])


