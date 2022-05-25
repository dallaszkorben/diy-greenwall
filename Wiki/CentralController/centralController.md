# Central Controller unit
The Central Controller is running on a Raspberry Pi Zero W

## Network configuration

### Install necessary SWs

```sh
    $ sudo apt update
    $ sudo apt full-upgrade
```
```sh
    # dnsmasq - This program has extensive features, but for our purposes we are using it as a DHCP server for our WiFi AP.
    # hostapd - This program defines our AP’s physical operation based on driver configuration. 

    $ sudo apt-get install dnsmasq hostapd     	
```


### Configurations

  * Check the existing network  
    This is what you can see before configuring
    ```sh
    pi@raspberrypi:~$ iw dev
    phy#0
        Unnamed/non-netdev interface
                wdev 0x4
                addr ba:27:eb:07:28:1f
                type P2P-device
                txpower 31.00 dBm
        Interface wlan0
                ifindex 2
                wdev 0x1
                addr b8:27:eb:ff:ff:ff
                ssid <YOUR HOME SSID> 
                type managed
                channel 1 (2437 MHz), width: 20 MHz, center1: 2437 MHz
                txpower 31.00 dBm
    ```
  * Configure dnsmasq  
Let’s call our new interface for AP to uap0
Here we can define the IP interval what we use for the nodes connecting to this AP. In this case it will be between 192.168.50.50 and 192.168.50.150
    ```sh
    pi@raspberrypi:~$ /etc/dnsmasq.conf
      interface=lo,uap0
      no-dhcp-interface=lo,wlan0
      bind-interfaces
      server=8.8.8.8
      domain-needed
      bogus-priv
      dhcp-range=192.168.50.50,192.168.50.150,24h
    ```

  * Configure hostapd  
Here the channel is hardcoded. There is a dynamic and better way to find out the right channel.
I’ll show it later
    ```sh
    pi@raspberrypi:~$ vi /etc/hostapd/hostapd.conf
      interface=uap0
      ssid=Central-Station-006 
      hw_mode=g 
      channel=1 
      macaddr_acl=0 
      auth_algs=1 
      ignore_broadcast_ssid=0 
      wpa=2 
      wpa_passphrase=viragfal 
      wpa_key_mgmt=WPA-PSK 
      wpa_pairwise=TKIP 
      rsn_pairwise=CCMP
    ```  

  * Configure wifi network interface file
    ```sh
     pi@raspberrypi:~$ vi /etc/wpa_supplicant/wpa_supplicant.conf

       ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev 
       update_config=1 

       network={ 
	       ssid="****" 
	       psk="****" 
	       key_mgmt=WPA-PSK 
	       id_str="AP1" 
       } 

       network={ 
	       ssid="****" 
	       psk="****" 
	       key_mgmt=WPA-PSK 
	       id_str="AP2" 
       }
 
  * Configure AP interface file
    ```sh       
     pi@raspberrypi:~$ vi /etc/network/interfaces
       source-directory /etc/network/interfaces.d 

       auto lo 
       auto uap0 
       auto wlan0 

       iface lo inet loopback 

       allow-hotplug uap0 
       iface uap0 inet static 
	       address 192.168.50.3 
	       netmask 255.255.255.0 
	       hostapd /etc/hostapd/hostapd.conf 

       allow-hotplug wlan0 
       iface wlan0 inet manual 
	       wpa-roam /etc/wpa_supplicant/wpa_supplicant.conf 

       iface AP1 inet dhcp 
       iface AP2 inet dhcp
     ```
  * Script to put all together
    ```sh
     pi@raspberrypi:~$ /usr/local/bin/hostapdstart.sh
       #!/bin/bash 

       mac=`sudo ifconfig |grep ether | sed 's/ether \([a-f0-9][a-f0-9]:[a-f0-9][a-f0-9]:[a-f0-9][a-f0-9]:[a-f0-9][a-f0-9]:[a-f0-9][a-f0-9]:[a-f0-9][a-f0-9]\).*/\1/g' | head -n 1` 

       sudo /sbin/iw phy phy0 interface add uap0 type __ap 
       sudo /bin/ip link set uap0 address $mac 

       sudo ifdown --force wlan0 
       sudo ifdown --force uap0 

       sudo ifup uap0 
       sudo ifup wlan0 

       # Fetch wifi channel 
       CHANNEL=`iwlist wlan0 channel | grep Current | sed 's/.*Channel \([0-9]*\).*/\1/g'` 
       export CHANNEL 

       # Create the config for hostapd 
       #cat /etc/hostapd/hostapd.conf.tmpl | envsubst > /etc/hostapd/hostapd.conf 

       # Uncomment the two following lines to get access to internet 
       #sysctl net.ipv4.ip_forward=1 
       #iptables -t nat -A POSTROUTING -s 192.168.50.0/24 ! -d 192.168.50.0/24 -j MASQUERADE 

       sudo systemctl restart hostapd 
       sleep 10 
       sudo systemctl restart dnsmasq 
       sleep 10 
       sudo systemctl restart dhcpcd
    ```
  * unmask hostapd
    ```sh
       pi@raspberrypi:~$ sudo systemctl unmask hostapd
       pi@raspberrypi:~$ sudo systemctl enable hostapd
       pi@raspberrypi:~$ sudo systemctl start hostapd
    ```
  * Run the script just after the reboot automatically  
    In the **crontab** file:
    ```sh
    root@raspberrypi:~$ crontab -e
       @reboot /usr/local/bin/hostapdstart.sh
    ```
  * Check the existing network after the configuration  
    You can see the new Interface: uap0
    ```sh
    root@raspberrypi:~# iw dev
       phy#0 
	       Unnamed/non-netdev interface 
		       wdev 0x3 
		       addr ba:27:eb:97:d5:fe 
		       type P2P-device 
		       txpower 31.00 dBm 
	       Interface uap0 
		       ifindex 3 
		       wdev 0x2 
		       addr b8:27:eb:97:d5:fe 
		       ssid Central-Station-006 
		       type AP 
		       channel 1 (2412 MHz), width: 20 MHz, center1: 2412 MHz 
		       txpower 31.00 dBm 
		       
               Interface wlan0
	               ifindex 2
                       wdev 0x1
                       addr b8:27:eb:ff:ff:ff
                       ssid <YOUR HOME SSID> 
                       type managed
                       channel 1 (2437 MHz), width: 20 MHz, center1: 2437 MHz
                       txpower 31.00 dBm		      
    ```

    ```sh
    root@raspberrypi:~# ip addr 
       1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000 
	       link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00 
	       inet 127.0.0.1/8 scope host lo 
		       valid_lft forever preferred_lft forever 
	       inet6 ::1/128 scope host
		       valid_lft forever preferred_lft forever 
       2: wlan0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000 
	       link/ether b8:27:eb:97:d5:fe brd ff:ff:ff:ff:ff:ff 
	       inet 192.168.0.103/24 brd 192.168.0.255 scope global dynamic wlan0 
		       valid_lft 1966sec preferred_lft 1966sec 
	       inet6 fdaa:bbcc:ddee:0:ba27:ebff:fe97:d5fe/64 scope global dynamic mngtmpaddr
		       valid_lft 2006054648sec preferred_lft 2006054648sec 
	       inet6 fe80::ba27:ebff:fe97:d5fe/64 scope link
		       valid_lft forever preferred_lft forever 
       3: uap0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000 
	       link/ether b8:27:eb:97:d5:fe brd ff:ff:ff:ff:ff:ff 
	       inet 192.168.50.3/24 brd 192.168.50.255 scope global uap0 
		       valid_lft forever preferred_lft forever 
	       inet6 fe80::ba27:ebff:fe97:d5fe/64 scope link
		       valid_lft forever preferred_lft forever

### Configuration hierarchy

```mermaid
graph LR
/var/spool/cron/crontabs/root --> /home/pi/Projects/diy-greenwall/Software/Central.AccessPoint-RaspberryPi/python/start
/var/spool/cron/crontabs/root --> /usr/local/bin/hostapdstart.sh

/usr/local/bin/hostapdstart.sh --> /etc/dnsmasq.conf
/usr/local/bin/hostapdstart.sh --> /etc/network/interfaces

/etc/network/interfaces --> /etc/hostapd/hostapd.conf
/etc/network/interfaces --> /etc/wpa_supplicant/wpa_supplicant.conf

  ```

---
## Controller software

### Create virtual environment for Python
```sh
pi@raspberrypi:~ $ sudo apt install python3-venv
pi@raspberrypi:~ $ cd /var/www/greenwall/python
pi@raspberrypi:/var/www/greenwall/python $ python3 -m venv env  
```

### Install prerequisites

  ```sh
  pi@raspberrypi:~ $ sudo apt-get install libapache2-mod-wsgi-py3
 
  pi@raspberrypi:/var/www/greenwall/python $ source env/bin/activate
  (env) pi@raspberrypi:/var/www/greenwall/python/env/bin $ pip install requests
  (env) pi@raspberrypi:/var/www/greenwall/python/env/bin $ pip3 install python-dateutil 
  (env) pi@raspberrypi:/var/www/greenwall/python/env/bin $ python -m pip install flask
  (env) pi@raspberrypi:/var/www/greenwall/python/env/bin $ pip install Flask-Classful==0.15.0b1
  (env) pi@raspberrypi:/var/www/greenwall/python/env/bin $ pip3 install -U flask-cors
  (env) pi@raspberrypi:/var/www/greenwall/python/env/bin $ pip3 install rpi_lcd
  (env) pi@raspberrypi:/var/www/greenwall/python/env/bin $ pip3 install evdev
  (env) pi@raspberrypi:/var/www/greenwall/python/env/bin $ pip3 install psutil
  (env) pi@raspberrypi:/var/www/greenwall/python/env/bin $ pip install scipy --no-cache-dir
  (env) pi@raspberrypi:/var/www/greenwall/python/env/bin $ pip install matplotlib
  (env) pi@raspberrypi:/var/www/greenwall/python/env/bin $ pip3 install pandas
  
  
  
  
  
  
  $ sudo apt-get install python3-sklearn python3-sklearn-lib  
  
  $ pip3 install opencv-python
  ```
### Clone the diy-greenwall  

First you should clone the diy-greenwall.
 ```sh
  $ cd
  $ mkdir Projects
  $ git clone https://github.com/dallaszkorben/diy-greenwall.git
 ```
As you need only the hierarcy under the **diy-greenwall/Software/Central.AccessPoint-RaspberryPi** folder, on the Rasberry Pi, you can filter out the not necesary parts. But it is not mandatory to do

```sh
  $ cd diy-greenwall
  $ git  filter-branch -f --subdirectory-filter Software/Central.AccessPoint-RaspberryPi 
```

Under the **python** folder, you can see the following hierarchy of the python code:
  ```sh
  .
  ├── config
  │   ├── config.py
  │   ├── ini_location.py
  │   ├── __init.py__
  │   ├── permanent_data.py
  │   ├── property.py
  │   └── __pycache__
  │       ├── config.cpython-37.pyc
  │       ├── ini_location.cpython-37.pyc
  │       ├── permanent_data.cpython-37.pyc
  │       └── property.cpython-37.pyc
  ├── controlbox
  │   ├── controlbox.py
  │   ├── __init__.py
  │   └── __pycache__
  │       ├── controlbox.cpython-37.pyc
  │       └── __init__.cpython-37.pyc
  ├── exceptions
  │   ├── __init.py__
  │   ├── invalid_api_usage.py
  │   └── __pycache__
  │       └── invalid_api_usage.cpython-37.pyc
  ├── graph
  │   ├── graph_level.py
  │   ├── __init.py__
  │   └── __pycache__
  │       └── graph_level.cpython-37.pyc
  ├── greenwall.wsgi
  ├── ky040
  │   ├── __init__.py
  │   ├── ky040.py
  │   └── __pycache__
  │       ├── __init__.cpython-37.pyc
  │       ├── ky040.cpython-37.pyc
  │       └── KY040.cpython-37.pyc
  ├── restserver
  │   ├── endpoints
  │   │   ├── ep_info_functions.py
  │   │   ├── ep_info_graph.py
  │   │   ├── ep_info_timestamp.py
  │   │   ├── ep_level_add.py
  │   │   ├── ep.py
  │   │   ├── __init.py__
  │   │   ├── __pycache__
  │   │   │   ├── ep.cpython-37.pyc
  │   │   │   ├── ep_info_functions.cpython-37.pyc
  │   │   │   ├── ep_info_graph.cpython-37.pyc
  │   │   │   ├── ep_info_level.cpython-37.pyc
  │   │   │   ├── ep_info_timestamp.cpython-37.pyc
  │   │   │   ├── ep_info_trend.cpython-37.pyc
  │   │   │   ├── ep_level_add.cpython-37.pyc
  │   │   │   └── ep_level_read.cpython-37.pyc
  │   │   ├── representations.py
  │   │   └── ~toDelete
  │   │       └── ep_info_level.py
  │   ├── gradual_thread_controller.py
  │   ├── __init.py__
  │   ├── __pycache__
  │   │   ├── gradual_thread_controller.cpython-37.pyc
  │   │   ├── representations.cpython-37.pyc
  │   │   ├── view_info.cpython-37.pyc
  │   │   ├── view_level.cpython-37.pyc
  │   │   └── ws_greenwall.cpython-37.pyc
  │   ├── representations.py
  │   ├── view_info.py
  │   ├── view_level.py
  │   └── ws_greenwall.py
  ├── start.py
  └── utilities
      ├── __init.py__
      ├── __pycache__
      │   └── report.cpython-37.pyc
      └── report.py  
  ```
  

### Install Web server on Raspberry Pi
  Apache2 server should be installed and configured to allow browsers to connect and see the statuses of Sensors

  * Find the codes under **web-location/greenwall/** folder
    ```sh
    .
    └── greenwall
        ├── favicon.ico
        ├── /graph-images
        ├── /index.html
        └── /script
            ├── /jquery
            │   └── jquery-3.6.0.min.js
            └── /jquery-ui
                ├── AUTHORS.txt
                ├── /external
                │   └── /jquery
                │       └── jquery.js
                ├── images              
                ├── index.html
                ├── jquery-ui.css
                ├── jquery-ui.js
                ├── jquery-ui.min.css
                ├── jquery-ui.min.js
                ├── jquery-ui.structure.css
                ├── jquery-ui.structure.min.css
                ├── jquery-ui.theme.css
                ├── jquery-ui.theme.min.css
                ├── LICENSE.txt
                └── package.json
    ```
  * Copy the the whole folder to /var/www folder
  
    ```sh
    pi@raspberrypi:~$ cd web-location
    pi@raspberrypi:web-location$ cp -r greenwall /var/www/
    ```

  * Configure available Apach2 config file  
    Alternativaly you can copy the **green-wall.conf** file, found under the **web-config** folder to the **/etc/apache2/conf-available** folder on the Raspberry pi
    ```sh
    pi@raspberrypi:~$ touch /etc/apache2/conf-available/green-wall.conf
     
    <VirtualHost *:80>
       ServerAdmin webmaster@greenwallsite.com
       ServerName www.greenwallsite.com
       ServerAlias greenwallsite.com

       ErrorLog /var/www/logs/error.log
       CustomLog /var/www/logs/access.log combined

       <IfModule dir_module>
           DirectoryIndex index.html
       </IfModule>

       Alias /greenwall/ /var/www/greenwall/
       <Directory /var/www/greenwall>
          Order allow,deny
          Allow from all
       </Directory>
    </VirtualHost>
    ```

  * Configure enabled Apach2 config file
    ```sh
    pi@raspberrypi:~$ ln -s /etc/apache2/conf-available/green-wall.conf /etc/apache2/conf-enabled/green-wall.conf      
    ```
  
  * Install mod_wsgi
    ```sh
    pi@raspberrypi:~$ sudo apt-get install libapache2-mod-wsgi python-dev
    ```

  * Enable mod_wsgi
    ```sh
    pi@raspberrypi:~$ sudo a2enmod wsgi 
    ```
      
  * Restart Apach2 service
    ```sh
    ~~pi@raspberrypi:~$ sudo /etc/init.d/apache2 restart~~ 
    pi@raspberrypi:~$ sudo systemctl restart apache2      
    ```

### Port forwarding
  Why do we need it?
  Because in  development/test phase I use the stand alone WSGI server to receive REST requests from the Sensor Stations and Control Stations. The stand alone WSGI server uses port 5000.
  But later, I use the integrated WSGI in the Apache server, instead of the stand alone WSGI. That means, the port changes to 80. But I do not want to change the code all the time in the Station modules, when I change the WSGI. 
To make it work in both case I have to do a port forwarding. If the Central Controler Unit receive a rest request to port 5000, it should be mapped to port 80 instead.

    ```sh
    root@raspberrypi:~# echo "1" /proc/sys/net/ipv4/ip_forward
    root@raspberrypi:~# iptables -t nat -A PREROUTING -p tcp -d 192.168.50.3 --dport 5000 -j DNAT --to-destination 192.168.50.3:80
    root@raspberrypi:~# iptables -t nat -A POSTROUTING -j MASQUERADE
    ```
Unfortunatelly this settings will disappear after a reset, so you have to make it persistent.





---
## ky040 - rotary encoder
  
  To enable/configure the rotary-encoder device tree overlay, simply put something like the following into **/boot/config.txt** (with the encoder connected to pins **5** and **6** on the Raspberry Pi)
  While you’re at it, you might also want to add the middle button as a key (mine is connected to pin **13**):

  * enable rotary encoder
    ```sh       
    pi@raspberrypi:~$ vi /boot/config.txt
       dtoverlay=rotary-encoder,pin_a=5,pin_b=6,relative_axis=1
       dtoverlay=gpio-key,gpio=13,keycode=28,label="ENTER"       
    ```
  After a reboot you’ll have a new device in **/dev/input/** for the rotary encoder. You can use the **evtest** tool (as in evtest /dev/input/event0) to look at the events it generates and confirm that it reacts perfectly to every turn of the encoder, without missing a movement or confusing the direction.

  * Here is an example, shows how to read the output of the rotary encoder.
    ```python
    from __future__ import print_function
    import evdev
    import select

    devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
    devices = {dev.fd: dev for dev in devices}
    value = 1
    print("Value: {0}".format(value))
    done = False
    
    while True:
        r, w, x = select.select(devices, [], [])
        for fd in r:
            for event in devices[fd].read():
                event = evdev.util.categorize(event)
                if isinstance(event, evdev.events.RelEvent):
                    value = value + event.event.value
                    print("Value: {0}".format(value))
                elif isinstance(event, evdev.events.KeyEvent):
                    if event.keycode == "KEY_ENTER" and event.keystate == event.key_up:
		        print("Enter")
    ```

---
## 2x16 LCD display
  
  * In the Raspberry Pi run the "Raspberry Pi Configuration" application and undert the "Interfaces" tab, **Enable** the I2C
  * Connect the pins of LCD display to the corresponding pins of RP
    * GND -> GND
    * VCC -> 5V
    * SDA -> SDA1
    * SCL -> SCL1
  * Check th eaddress of the I2C box on the RP
    ```sh         
    pi@raspberrypi:/var/www $ i2cdetect -y 1
         0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
    00:          -- -- -- -- -- -- -- -- -- -- -- -- -- 
    10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
    20: -- -- -- -- -- -- -- 27 -- -- -- -- -- -- -- -- 
    30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
    40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
    50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
    60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
    70: -- -- -- -- -- -- -- --                       
    ```
    






