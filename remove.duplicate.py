# Kuznik Jakub
# KNOT - product_reviews_in_czech
# xkuzni04@stud.fit.vutbr.cz
# This script should get all the zbozi.cz reviews 
# xkuzni04@stud.fit.vutbr.cz

# Every server gets throught urls in 
# logs_and_input_files/input_files_for_each_server/

from collections import OrderedDict
from datetime import date, timedelta
import json 
from urllib.parse import uses_fragment
import requests
import time
import argparse
import socket
import sys
import os
from typing import List, Any
from urllib.request import urlopen

sys.path.insert(0, '.')

import collections
orderedDict = collections.OrderedDict()
from collections import OrderedDict

import shutil

def line_prepender(line, file):
    with open(file, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip('\r\n') + '\n' + content)
    f.close()

def line_appender(line, file):
    with open(file, 'a') as f:
        f.write(line)
    f.close()

def tempo_file():
    original = "all_zbozi.cz_reviews.log"
    target = "temp_reviews_log"
    shutil.copyfile(original, target)

def fix_space():
    file = open('temp_reviews_log', 'r')
    n = 0
    while 1:
        # read by character
        char = file.read(1)         
        if not char:
            break
        if char == '}':
            char = file.read(1)
            while 1:
                if char == ',':
                    break
                if char == ' ':
                    char = file.read(1)
                    continue
                elif char == '\n':
                    n = n+1
                    char = file.read(1)
                    continue
                elif char == '{':
                    print(char, n)
                    
                    char = file.read(1)
                    break
                else:
                    break 
        if char == '\n':
            n = n+1

    file.close()


def main():
    tempo_file()

    tf = "temp_reviews_log" #temp file

    line_prepender("[", tf )
    line_appender("]", tf)

    fix_space()
    #TODO PRIDAT DELIMETRY  },{review{}
    #Najít radky a pridat carky na dane rádky 

    tempf = open(tf, 'r')
    data = tempf.read()
    json_data = json.loads(data)
    print(json_data)
    tempf.close()




if __name__ == '__main__':
    start = time.time()
    main()
    print(time.time() - start)
