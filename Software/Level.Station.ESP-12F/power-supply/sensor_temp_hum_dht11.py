from machine import Pin
import dht

class SensorTempHum():

    def __init__(self, dataGpio):

        dataPin = Pin(dataGpio)
        self.sensor = dht.DHT11(dataPin)

    def getTempHum(self):

        try:
            self.sensor.measure()
            temp = self.sensor.temperature()
            hum = self.sensor.humidity()
            #temp_f = temp * (9/5) + 32.0
        except OSError as e:
            temp = None
            hum = None

        return temp, hum


