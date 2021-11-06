# diy-greenwall

## Frame of the green wall

## HW support for the green wall

## ESP-12F

### Install SW on ESP-12F

* Find the codes for ESP-12F: <b>Software/Level.Station.ESP-12F/power-supply/</b>  
boot.py  
config.py  
control.py  
level.config.json  
level.py  
read.me  
ultrasonic_sensor.py*  
water_level_sensor.py*  
wifi_level.py  


* Do the settings in the config file: <b>level.config.json</b>
```json
{
    "central-ap":{
        "essid": "Central-Station-001",                  # [Modify it according to the Raspberry Access Point]
        "password": "****"                               # [Modify it according to the Raspberry Access Point]
        "webserver-ip": "192.168.50.3:5000",             # [Modify it according to the Raspberry node]
        "webserver-path-level-report": "level/add"       # [Leave it]
    },
    "level-sta":{
        "analog-pin": 0,                                 # [Leave it]
        "trigger-pin": 5,                                # [Leave it]
        "echo-pin": 4,                                   # [Leave it]
        "led-status-pin": 2,                             # [Leave it]
        "led-status-inverse": true,                      # [Leave it]
        "report-interval-sec": 50                        # [Leave it]
    },
    "level-sensor":{
        "zero-level": 59,                                # [Leave it]
        "linear-m": 0.11,                                # [Leave it]
        "linear-b": -35,                                 # [Leave it]
        "sample-number": 100,                            # [Leave it]
        "maximum-variance": 0.1                          # [Leave it]
    }
}
``` 
* Connect your ESP-12F to your Linux machine through USB
* Check which USB dev used for that
```
username@machine:~$ dmesg


[1204048.025087] usb 4-1: USB disconnect, device number 25
[1204048.025326] ch341-uart ttyUSB0: ch341-uart converter now disconnected from ttyUSB0
[1204048.025351] ch341 4-1:1.0: device disconnected
[1204050.213052] usb 4-1: new full-speed USB device number 26 using uhci_hcd
[1204050.400070] usb 4-1: New USB device found, idVendor=1a86, idProduct=7523, bcdDevice= 2.54
[1204050.400074] usb 4-1: New USB device strings: Mfr=0, Product=2, SerialNumber=0
[1204050.400076] usb 4-1: Product: USB2.0-Ser!
[1204050.403128] ch341 4-1:1.0: ch341-uart converter detected
[1204050.410111] usb 4-1: ch341-uart converter now attached to ttyUSB0

```
* Copy the files, one by one, into the ESP-12F through <span style="color:green">/dev/ttyUSB0</span> - in our case - using the ampy app.
```sh
username@machine:~$ ampy -p /dev/ttyUSB0 put ./level.py
```
* Reset your ESP-12F pushing the "Reset" button
* Now you can disconnect the ESP-12F from your machine and use it alone providing power supply  
You can see the onboard blue led blinking. If it is ON just a short time and then 1 sec OFF for 10 seconds and then ON about 1-2 seconds, it means the ESP-12F found the server, successfully connected and sent data.


You can check what the code is doing if you plugin the ESP-12F again into your Linux machine, and you connect tho the ESP-12F through serial port using the picocom app.
```python
username@machine:~$ picocom /dev/ttyUSB0 -b115200
picocom v3.1

port is        : /dev/ttyUSB0
flowcontrol    : none
baudrate is    : 115200
parity is      : none
databits are   : 8
stopbits are   : 1
escape is      : C-a
local echo is  : no
noinit is      : no
noreset is     : no
hangup is      : no
nolock is      : no
send_cmd is    : sz -vv
receive_cmd is : rz -vv -E
imap is        : 
omap is        : 
emap is        : crcrlf,delbs,
logfile is     : none
initstring     : none
exit_after is  : not set
exit is        : no

Type [C-a] [C-h] to see available commands
Terminal ready
�������������������
```
stop it by [Ctrl]c
and then restart again by [Ctrl]d
  
```python  
�������������������
KeyboardInterrupt: 

MicroPython v1.14 on 2021-02-02; ESP module with ESP8266
Type "help()" for more information.
>>> 
MPY: soft reboot

connecting to network \
ip:  192.168.50.112 - POST http://192.168.50.3:5000/reportlevel/set: 200
ip:  192.168.50.112 - POST http://192.168.50.3:5000/reportlevel/set: 200
...
```


## Raspberry Pi Zero W

### Install SW on Raspberry Pi
