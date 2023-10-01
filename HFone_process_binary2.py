#!/usr/bin/python3

import numpy as np
import struct
import time
import os, sys
#import pigpio
import pickle as pic
from datetime import datetime, timedelta

LO_LO = 10782.72 #10410
LO_HI = 10782.72 #10410

#pi = pigpio.pi()  # Get instance of the pigpio.pi
#pi.hardware_PWM(13, 0, 500000) # Set PWM on
tone = False       # No tone so LO is low
LO = LO_LO

Transits_dir = '/data/Starlink_Detector/Transits'

tod = datetime.now()  
datestr = tod.strftime("%y%m%d/%H")  # As date as string to check

# Check if day exists in directory structure
transit_hour_dir = f"{Transits_dir}/{datestr}"

if not os.path.exists(transit_hour_dir):
    print(transit_hour_dir,"doesn't exist")    
    sys.exit(-1)

datestr = tod.strftime("%y%m%d_%H00")
hour = tod.strftime("%H")  # To check if hour changes

out_file = f"{transit_hour_dir}/HackRF_{datestr}.npy" 

#if os.path.exists(out_file): # Check if exists 
    
pf = open(out_file,'ab+')
print(f"{transit_hour_dir}/HackRF_{datestr}.npy")

# Get record size and lo and hi edges
data = sys.stdin.buffer.read(20)
rlen, nu_lo, nu_hi = struct.unpack('<IQQ',data[:20])
nu_edge = nu_lo

print(rlen, nu_lo, nu_hi)
nu = (nu_lo+nu_hi)/2

# Get rest of record
print('hello')
data = sys.stdin.buffer.read(rlen-16)
vals = struct.iter_unpack('<f',data[:])

val = 0
nv = 0

for v in vals:
    val += v[0]
    nv += 1
    
val /= nv


# Initialize lists to store freq and amps

freq = []
freq.append(nu)

amps = []
amps.append(val)


# Now loop to keep reading records from stream

while True:
    data = sys.stdin.buffer.read(20)
    rlen, nu_lo, nu_hi = struct.unpack('<IQQ',data[:20])

    # Get rest of record
    data = sys.stdin.buffer.read(rlen-16)
    vals = struct.iter_unpack('<f',data[:])
    
    
    if nu_lo==nu_edge:  # Back at start
        
        # Need to dump data
        freq = np.array(freq)
        amps = np.array(amps)
        
#        print(f"freq {freq}")
#        np.save(pf,(tod, freq, amps, LO), allow_pickle=True)
        pic.dump((tod, freq, amps, LO), pf)
        pf.flush()

        tod = datetime.now()  
        hr = tod.strftime("%H")

        freq = []
        amps = []

        if tone:         # Change tone state
            tone = False
 #           pi.hardware_PWM(13, 0, 500000)      # Turn tone off
            LO = LO_LO
        else:
            tone = True
 #           pi.hardware_PWM(13, 22000, 500000)  # Turn tone on
            LO = LO_HI
            

    #    print(hr,hour)
        if hr != hour:  # Time to change hour
            hour = hr
            
            datestr = tod.strftime("%y%m%d/%H")

            transit_hour_dir = f"{Transits_dir}/{datestr}"
            if not os.path.exists(transit_hour_dir):
                print(transit_hour_dir,"doesn't exist")
                sys.exit(-1)
                        
            datestr = tod.strftime("%y%m%d_%H%M")
            pf = open(f"{transit_hour_dir}/HackRF_{datestr}.npy",'wb')
            print(f"{transit_hour_dir}/HackRF_{datestr}.npy")
    
    nu = (nu_lo+nu_hi)/2

    val = 0
    nv = 0

    for v in vals:
        val += v[0]
        nv += 1
    
    val /= nv

        
    freq.append(nu)
    amps.append(val)

   
