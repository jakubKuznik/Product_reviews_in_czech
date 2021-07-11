# Kuznik Jakub
# KNOT - product_reviews_in_czech
# xkuzni04@stud.fit.vutbr.cz
# This script should get all the zbozi.cz urls
# xkuzni04@stud.fit.vutbr.cz

# Script should get through all the categories from input file: all_zbozi.cz_products_url
# And download all the products from zbozi.cz and store them to : all_zbozi.cz_products_url


import time
import socket
import sys
import argparse
import os
from typing import List, Any

sys.path.insert(0, '.')

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains


# TESTING - CHROME MODE
##################################
#options = Options()
#options.binary_location = "/usr/bin/google-chrome"    #chrome binary location specified here
#options.add_argument("--no-sandbox") #bypass OS security model
#options.add_argument("--disable-dev-shm-usage") #overcome limited resource problems
#options.add_experimental_option("excludeSwitches", ["enable-automation"])
#options.add_experimental_option('useAutomationExtension', False)
#options.add_argument("start-maximized")
#options.add_argument("disable-infobars")
#options.add_argument("--disable-extensions")
#driver = webdriver.Chrome('drivers/chromedriver', options=options)
#################################################

# RUN ON MINERVA - CHROME MODE
################################################
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.binary_location = '/usr/bin/google-chrome'
path_to_chromedriver = '/usr/bin/chromedriver'
chrome_driver = '/mnt/minerva1/nlp/projects/imdb_reviews/chromedriver_86'
path_to_chrome_driver = 'drivers/chromedriver'
os.environ["webdriver.chrome.driver"] = path_to_chrome_driver
driver = webdriver.Chrome(path_to_chrome_driver, options=options)
##################################################

catlist = []

#Download all the products from given category
def get_product_urls(category, output_file):

    try:
        driver.get(str(category))
    except:
        return

    time.sleep(1)

    while True:
        try:
            time.sleep(0.1)
            # Scroll down to last name in list
            page = driver.find_elements_by_xpath("//a[@href]")
            driver.execute_script("window.scrollTo(0, window.scrollY + 400)")
            #try:
            for elem in page:
                filter_elem = elem.get_attribute("href")
                if filter_elem not in catlist and "vyrobek" in str(filter_elem):
                    catlist.append(filter_elem)
                    print(filter_elem,";",category)
                    output_file.write("%s;%s" %(filter_elem, category))
                #except:
                    #continue
        except:
            break
        try:
            time.sleep(2)
            elm = driver.find_element_by_class_name('next')
            time.sleep(2)
            elm.click()
            time.sleep(2)
        except:
            print("Cannot open page")
            break
    return


# Check if output files can be open
def output_files_open():
    try:
        outfile = open("logs_and_input_files/all_zbozi.cz_products_url", 'a')
    except IOError:
        sys.stderr.write("Cannot open outfile")
        return False
    return outfile


# Check if input file can be open
def read_file_open(server_host_name):
    path = "logs_and_input_files/input_files_for_each_server_products/"
    path = path + server_host_name
    print(path)
    try:
        read_file = open(path, 'r')
    except IOError:
        sys.stderr.write("Cannot open readfile")
        return False
    return read_file



# Ve ll need just url that contains word "vyrobek"
def filter_urls(urls, substring):
    out = []
    for url in urls:
        if substring in url:
            out.append(url)

    return out

#Get next category from file
def get_next_category(category_file):
    return category_file.readline()

## 
# Parse arguments'
def parse_args():
        
        parser = argparse.ArgumentParser(description='KNOT - product reviews in czech - Author: Jakub Kuzník {xkuzni04} \
        ', add_help=False)
        parser.add_argument("-h", "--help", action="count", default=0, help="tisk napovedy")
        
        try:
                args = parser.parse_args()
        except:
                sys.exit(1)

        if(args.help == 1):
                if(len(sys.argv) == 2):
                        parser.print_help()
                        print("\n\nProgram otevře vstupní soubor který je stejný jako hostname serveru logs_and_input_files/input_files_for_each_server_products/hostname\nPostupně začne ukládat veškeré url jednotlivých produktů do souboru logs_and_input_files/all_zbozi.cz_products_url \n")
                        sys.exit(0)
                else:
                        print("Error: Help with other argument", file=sys.stderr)
                        sys.exit(1)

        return args

def main():

    parse_args()

    # Get system hostname becouse every knot server has its own input file 
    server_host_name = socket.gethostname()
    print(server_host_name)

    # Open output files
    if output_files_open() == False: sys.exit(2)  # check if files for output can be open
    output_file = output_files_open()

    if read_file_open(server_host_name) == False: sys.exit(2)  # check if files for tput can be open
    category_file = read_file_open(server_host_name) #

    for i in range(2140):
        get_product_urls(get_next_category(category_file), output_file)


    output_file.close()
    category_file.close()
#    display.stop()

if __name__ == '__main__':
    start = time.time()
    main()
    print(time.time() - start)
