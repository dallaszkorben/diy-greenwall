#! /bin/sh

esptool.py --port /dev/ttyUSB0 --baud 460800 write_flash --flash_size=detect 0 ~/Downloads/image_files/esp8266-20210202-v1.14.bin

echo "boot.py"
ampy -p /dev/ttyUSB0 put ./boot.py

echo "common.py"
ampy -p /dev/ttyUSB0 put ./common.py

echo "config.py"
ampy -p /dev/ttyUSB0 put ./config.py

echo "control.config.json"
ampy -p /dev/ttyUSB0 put ./control.config.json

echo "control_station.py"
ampy -p /dev/ttyUSB0 put ./control_station.py

echo "lamp_control.py"
ampy -p /dev/ttyUSB0 put ./lamp_control.py

echo "representations.py"
ampy -p /dev/ttyUSB0 put ./representations.py

echo "web_server.py"
ampy -p /dev/ttyUSB0 put ./web_server.py

echo "wifi_control.py"
ampy -p /dev/ttyUSB0 put ./wifi_control.py
