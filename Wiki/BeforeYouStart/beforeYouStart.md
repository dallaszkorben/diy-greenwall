# Before you start

I'm working on Ubuntu 22.04.1 LTS 
You need to install some things and fix some other things to be able to start

## Arduino

### Install Arduino

```sh
$ sudo apt update
$ sudo apt upgrade
$ mkdir arduino
$ cd arduino/
$ wget https://downloads.arduino.cc/arduino-1.8.15-linux64.tar.xz
$ tar -xvf ./arduino-1.8.15-linux64.tar.xz
$cd arduino-1.8.15/
$ sudo ./install.sh
```

### Add necessary Boards

File > Preferences > Additional Boards Manager URLs:

https://dl.espressif.com/dl/package_esp32_index.json,https://arduino.esp8266.com/stable/package_esp8266com_index.json


### Install necessary Libraries

Tools > Manager Libraries

 * BMP180MI
 * ArduinoJson
 * DHT sensor library
 * Preferences
 * Time


### Fix ttyUSB error

It might happen that when you upload a sketch - after you have selected your board and the serial port -, you get an error Error opening serial port ... If you get this error, you need to set serial port permission.

Check the serial port permission:

```sh
$ ls -l /dev/ttyUSB0
crw-rw---- 1 root dialout 188, 0 Nov 12 21:36 /dev/ttyUSB0
```

You need to add your user to the group
<username>: is your Linux user name.

```sh
sudo usermod -a -G dialout <username>
```

You will need to log out and log in again for this change to take effect.
And then you cna start the arduino UI again




