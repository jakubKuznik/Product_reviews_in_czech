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
from os import read 
from urllib.parse import uses_fragment
import time
import sys
from typing import List, Any
from urllib.request import urlopen
from time import sleep
sys.path.insert(0, '.')

import collections
orderedDict = collections.OrderedDict()
from collections import OrderedDict
import shutil
import glob
# Global variable that save on which lines are each json ends 
lines = [] 


#
def line_prepender(line, file):
    with open(file, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip('\r\n') + content)
    f.close()

def line_appender(line, file):
    with open(file, 'a') as f:
        f.write(line)
    f.close()

def tempo_file():
    original = "all_zbozi.cz_reviews.log"
    target = "temp_reviews_log"
    shutil.copyfile(original, target)

def find_space():
    file = open('temp_reviews_log', 'r')
    n = 0
    while 1:
        # read by character
        char = file.read(1)         
        if not char:
            break
        if char == '}':
            char = file.read(1)
            n = n+1
            while 1:
                if char == ',':
                    break
                if char == ' ':
                    char = file.read(1)
                    n = n+1
                    continue
                elif char == '\n':
                    char = file.read(1)
                    n = n+1
                    continue
                elif char == '{':
                    lines.append(n) 
                    char = file.read(1)
                    n = n+1
                    break
                else:
                    break 

        n = n+1
    file.close()

# Store nth json file from temp_revies_log to temp_one_json
def get_nth_json_file(index):

    if index >= len(lines):
        return

    file = open('temp_reviews_log', 'r')
    # clear file 

    # append character by character
    file_out = open(str(index) + ".json", "w")
    file_out.close()

    file_out = open(str(index) + ".json", 'a')

    if index == 0:
        start = 0
    else:
        start = lines[index-1]
        start = start

    end = lines[index]
    end = end - 1
    n = 0
    
    while 1:
        char = file.read(1)
        if n == start:
            break
        n = n+1

    char = ''
    while 1:
        char = file.read(1)
        file_out.write(char)
        n += 1
        if n == end:
            break
        if char == '':
            break

    file_out.close()
    line_prepender("{", str(index) + ".json")
    file.close()

# Get throw all the json store them to tempo file and append them to final_json 
def create_final_json():

    read_files = glob.glob("*.json")
    output_list = []

    for f in read_files:
        with open(f, "rb") as infile:
            output_list.append(json.load(infile))

    with open('final_json', 'w', encoding='utf-8') as f:
        json.dump(output_list, f, ensure_ascii=False, indent=4)


def main():

    # Copy all revies file to temp file
    tempo_file()

    #temp file
    tf = "temp_reviews_log" 


#    line_prepender("{", tf )
#    line_appender("]", tf)

    # Find where each json file ends and store that character postition to lines []
    find_space()

    n = 0
    while 1:
        get_nth_json_file(n)
        n += 1
        if n >= len(lines):
            break     


    create_final_json()
    # Get throw all the json store them to tempo file and append them to final_json 
    #create_final_json()

if __name__ == '__main__':
    start = time.time()
    main()
    print(time.time() - start)
