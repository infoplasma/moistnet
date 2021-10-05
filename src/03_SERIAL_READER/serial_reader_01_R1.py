import serial
import colorama as clr
import re
import csv
from datetime import datetime
from re import match


_PATTERN = "^([-+]?\d+(\.\d+)?\,){7}([-+]?\d+(\.\d+)?)$"

with serial.Serial('/dev/ttyUSB0', 115200, timeout=1) as ser:

    while True:
        raw_data = ""
        data = [""]
        
        raw_data = ser.readline().decode().strip()
        
        if match(_PATTERN, raw_data) is not None:
            print(clr.Fore.RED + "{:%Y%m%d-%H%M%S}: ".format(datetime.now()), end='')
            print(clr.Fore.GREEN + raw_data)
        
            with open("/mnt/upy_rpi_moist_data_R1.csv", "a+") as f:
                w = csv.writer(f)
                data = raw_data.split(",")
                data.insert(0, "{:%Y%m%d%H%M%S}".format(datetime.now()))
                w.writerow(data)                
        else:
            pass
