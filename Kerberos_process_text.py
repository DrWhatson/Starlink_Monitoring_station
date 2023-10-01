#!/usr/bin/env python3

import numpy as np
import struct
import time
import os, sys
import pickle as pic
from datetime import datetime, timedelta

Transits_dir = '/data/Starlink_Detector/Transits'

data = sys.stdin.readline()  # get line
word = data.split(',')
date_str = word[0]
time_str = word[1]

yr= date_str[2:4]
mo = date_str[5:7]
dy = date_str[8:10]
hr = time_str[1:3]
mi = time_str[4:6]

datestr = f"{yr}{mo}{dy}/{hr}"

# Check if day exists in directory structure
transit_hour_dir = f"{Transits_dir}/{datestr}"

#hour = tod.strftime("%H")  # To check if hour changes

if not os.path.exists(transit_hour_dir):
    print(transit_hour_dir,"doesn't exist")    
    sys.exit(-1)

datestr = f"{yr}{mo}{dy}_{hr}00"
#datestr = tod.strftime("%y%m%d_%H%M")

pf = open(f"{transit_hour_dir}/Kerberos_{datestr}.csv",'a+')
print(f"{transit_hour_dir}/Kerberos_{datestr}.csv")

pf.write(f"{data}")

hour = hr

# Now loop to keep reading records from stream

while True:
    data = sys.stdin.readline()
    word = data.split(',')
    
    date_str = word[0]
    time_str = word[1]
    hr = time_str[1:3]
    
           
    #    print(hr,hour)
    if hr != hour:  # Time to change hour
        hour = hr
        yr = date_str[2:4]
        mo = date_str[5:7]
        dy = date_str[8:10]
        mi = time_str[4:6]
            
        datestr = f"{yr}{mo}{dy}/{hr}"
        transit_hour_dir = f"{Transits_dir}/{datestr}"
        if not os.path.exists(transit_hour_dir):
            print(transit_hour_dir,"doesn't exist")
            sys.exit(-1)
                        
        datestr = f"{yr}{mo}{dy}_{hr}{mi}"
        pf = open(f"{transit_hour_dir}/Kerberos_{datestr}.csv",'w')
        print(f"{transit_hour_dir}/Kerberos_{datestr}.csv")
    
        
    pf.write(f"{data}")


   