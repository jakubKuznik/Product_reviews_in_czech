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
import time
import sys
from typing import List, Any
from urllib.request import urlopen

sys.path.insert(0, '.')

import collections
orderedDict = collections.OrderedDict()
from collections import OrderedDict
import shutil



lines = [] 

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
    
def get_nth_json_file(index):

    if index >= len(lines):
        return
    file = open('temp_reviews_log', 'r')

    file_out = open('temp_one_json', 'w')
    file_out.close()
    
    file_out = open('temp_one_json', 'a')

    if index == 0:

        start = 0
    else:
        start = lines[index-1]
        start = start -1

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
    file.close()

def create_final_json():

    result = []
    n = 0
    while 1:
        get_nth_json_file(n)
        with open("temp_one_json", "rb") as infile:
            result.append(json.load(infile))
        n += 1
        if n == len(lines):
            return 

    with open("final_json", "wb") as outfile:
        json.dump(result, outfile)





def main():
    tempo_file()

    tf = "temp_reviews_log" #temp file

    line_prepender("[", tf )
    line_appender("]", tf)

    find_space()
    
    
    get_nth_json_file(len(lines))
    create_final_json()


if __name__ == '__main__':
    start = time.time()
    main()
    print(time.time() - start)
