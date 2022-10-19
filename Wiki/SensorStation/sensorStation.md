# Sensor Station
The Sensor Station units are ESP12F modules.
The code is written in C under Arduino.

## Needed libraries in Arduino

## WebServer entry points


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




