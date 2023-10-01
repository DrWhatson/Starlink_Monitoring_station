# Starlink_Monitoring_station

This repro provides a very basic monitoring of Starlink and Oneweb satellites using a TV satellite LNB connected to a SDR receiver for beacons and a HackRF One for scanning of downlnk usage

The current system runs on a 2GB Raspberry Pi 4 using ubuntu 22.04

## Install basic stuff
>sudo apt-get install libusb-1.0-0-dev git cmake

##  Install python goodies
>sudo apt install python3-pip python3-pyqt4 build-essential gfortran >libatlas3-base libatlas-base-dev python3-dev python3-setuptools libffi6 >libffi-dev python3-tk pkg-config libfreetype6-dev php-cli wondershaper


## Install Hackrf software
>sudo apt-get install hackrf


## Install skyfields module
>sudo apt install python3-skyfield


## Install a webserver
>sudo apt install lighttpd

Edit /etc/lighttpd/lighttpd.conf to point at monitoring webpage

server.document-root        = "/data/webpages"

## Crontab setup

>5 23 * * * /Starlink_Detector/bin/get_TLEs 1
>30 * * * * /Starlink_Detector/bin/get_Transits 0
>*/10 * * * * /Starlink_Detector/bin/Plot_all_10m


## Initial setup

To get TLE for today
bin/get_TLEs 0 

To get transit times for present hour
bin/get_Transits 1


## Launch preocesses

python3 launch_SDRs.py > output.log 2>&1 &