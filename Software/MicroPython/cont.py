import time
from ultrasonic_sensor import UltrasonicSensor as Ultra

GPIO_TRIGGER_1 = 5
GPIO_ECHO_1 = 4

def cont():
    ultra1 = Ultra(GPIO_TRIGGER_1, GPIO_ECHO_1)

    while True:
        time.sleep_ms(1000)
        print(ultra1.getDistanceMeanInMm())
#        print(ultra1.getDistanceInMm())