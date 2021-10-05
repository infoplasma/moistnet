#!/usr/bin/env python3

import serial
import colorama as clr
import re
import csv
from datetime import datetime
from re import match


_PATTERN = "^([-+]?\d+(\.\d+)?\,){7}([-+]?\d+(\.\d+)?)$"
_SERIAL_PORT = '/dev/ttyUSB0'
_BAUDRATE = 115200
_WRITE_FILE = "/home/pi/uPY-PROJECTS/moistnet/05_DATA_FILEs/moist_data.csv"

print("*** READING TO PORT: {} @{}BAUD".format(_SERIAL_PORT, _BAUDRATE))
print("*** WRITING TO FILE: {}".format(_WRITE_FILE))

with serial.Serial(_SERIAL_PORT, _BAUDRATE, timeout=1) as ser:

    while True:
        raw_data = ""
        data = [""]
        
        raw_data = ser.readline().decode().strip()
        
        if match(_PATTERN, raw_data) is not None:
            print(clr.Fore.RED + "{:%Y%m%d-%H%M%S}: ".format(datetime.now()), end='')
            print(clr.Fore.GREEN + raw_data)
        
            with open(_WRITE_FILE, "a+") as f:
                w = csv.writer(f)
                data = raw_data.split(",")
                data.insert(0, "{:%Y%m%d%H%M%S}".format(datetime.now()))
                w.writerow(data)                
        else:
            pass
