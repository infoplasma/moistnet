#!/usr/bin/env python3

import serial
import colorama as clr
import re
import csv
from datetime import datetime
from re import match


PATTERN = "^([-+]?\d+(\.\d+)?\,){7}([-+]?\d+(\.\d+)?)$"
SERIAL_PORT = '/dev/ttyUSB0'
BAUDRATE = 115200
WRITE_FILE = "/home/pi/SHARES/PUBLIC/basti_data/moist_data.dat"

print("*** READING TO PORT: {} @{}BAUD".format(SERIAL_PORT, BAUDRATE))
print("*** WRITING TO FILE: {}".format(WRITE_FILE))

with serial.Serial(SERIAL_PORT, BAUDRATE, timeout=1) as ser:

    while True:
        raw_data = ""
        data = [""]
        
        raw_data = ser.readline().decode().strip()
        if match(PATTERN, raw_data) is not None:

            print(clr.Fore.RED + "{:%Y%m%d-%H%M%S}: ".format(datetime.now()), end='')
            print(clr.Fore.GREEN + raw_data)
        
            with open(WRITE_FILE, "a+") as f:
                w = csv.writer(f)
                data = raw_data.split(",")
                data.insert(0, "{:%Y%m%d%H%M%S}".format(datetime.now()))
                w.writerow(data)                
        else:
            pass
