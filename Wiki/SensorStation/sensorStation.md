# Sensor Station
The Sensor Station units are ESP12F modules.
The code is written in C under Arduino.

## Needed libraries in Arduino

## WebServer entry points
You can send direct REST requests to the SensorStation

### GET /configure
```sh
pi@raspberrypi:~ $ curl -s --request GET http://192.168.50.101:80/configure
{"stationId": "default","sensorTempHumOutGPIO": "0","sensorDistanceTrigGPIO": "12","sensorDistanceEchoGPIO": "14","intervalReportMillis": "600300","intervalRegisterMillis": "120600",}
```

### POST /configure
```sh
```

### GET /temperature
```sh
pi@raspberrypi:~ $ curl -s --request GET http://192.168.50.101:80/temperature
{"temperature": "24.15"}
```

### GET /humidity
```sh
pi@raspberrypi:~ $ curl -s --request GET http://192.168.50.101:80/humidity
{"humidity": "45.00"}
```

### GET /pressure
```sh
pi@raspberrypi:~ $ curl -s --request GET http://192.168.50.101:80/pressure
{"pressure": "102545.00"}
```

### GET /distance
```sh
pi@raspberrypi:~ $ curl -s --request GET http://192.168.50.101:80/distance
{"distance": "7.21"}
```

### GET /all/actual
```sh
pi@raspberrypi:~ $ curl -s --request GET http://192.168.50.101:80/all/actual
{"temperature": "24.20","humidity": "45.70","pressure": "102549.00","distance": "7.62",}
```

### GET /all/aggregated
```sh
pi@raspberrypi:~ $ curl -s --request GET http://192.168.50.101:80/all/aggregated
{"temperature": "24.17","humidity": "45.92","pressure": "102546.05","distance": "7.27",}
```

## Configure Sensor Station


## Sensors

### Temperature and Humidity

### Air pressure and Temperature

### Distance/Water level


## Wiring

```sh
ESP12F       | DHT22  BMP180  HCSR04                           
             |                                                       
pin Function |                                       
_____________|______________________
 D3 GPIO 0   | OUT                                               
             |                                                         
 D2 GPIO 4   |        SDA                                       
 D1 GPIO 5   |        SCL                     
             |                                
 D5 GPIO 14  |                ECHO            
 D6 GPIO 12  |                TRIG            
                                              
                                              
    HCSR04                      ESP12F                             BMP180
 .----------.           .---------------------.
 |          |           |    || |_| |_| |     |               .--------------.
 |          |           | o  ||         |TX o |               |              |
 |          |           | o   .--------.    o |               | o VIN     O  |
 |   GND  o------.      | o   |        |    o |       .---------o GND        |
 |   Echo o---------------o D5|        |D01 o---------|---------o SCL  .---. |
 |   Trig o---------------o D6|        |D02 o---------|---------o SDA  |   | |
 |   Vcc  o----. |      | o   |        |D03 o---------|--.    |        `---' |
 |          |  | |      | o   .--------'GND o---------.  |    `--------------'
 |          |  | | .------o 3.3V        5V  o----.    |  |
 |          |  | | |    |                     |  |    |  |         DHT22
 |          |  | | |    |                     |  |    |  |    . -------------.
 `----------'  | | |    `---------------------'  |    |  |    |           |   \
               | | `-----------------------------|----|--|------o +       |    \
               `---------------------------------'    |  `------o Out     | O  | 
                 `------------------------------------`---------o -       |    /
                                                              |           |   /
                                                              `--------------'

```




