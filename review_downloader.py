# Kuznik Jakub
# KNOT - product_reviews_in_czech
# xkuzni04@stud.fit.vutbr.cz
# This script should get all the zbozi.cz reviews 
# xkuzni04@stud.fit.vutbr.cz

# Every server gets throught urls in 
# logs_and_input_files/input_files_for_each_server/


import time
import socket
import sys
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
options = Options()
options.binary_location = "/usr/bin/google-chrome"    #chrome binary location specified here
options.add_argument("--no-sandbox") #bypass OS security model
options.add_argument("--disable-dev-shm-usage") #overcome limited resource problems
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
driver = webdriver.Chrome('drivers/chromedriver', options=options)
#################################################

# RUN ON MINERVA - CHROME MODE
################################################
#options = Options()
#options.add_argument('--headless')
#options.add_argument('--no-sandbox')
#options.add_argument('--disable-dev-shm-usage')
#options.binary_location = '/usr/bin/google-chrome'
#path_to_chromedriver = '/mnt/minerva1/knot/projects/product_reviews_in_czech/drivers/chromedriver'
#chrome_driver = '/mnt/minerva1/nlp/projects/imdb_reviews/chromedriver_86'
#path_to_chrome_driver = 'drivers/chromedriver'
#os.environ["webdriver.chrome.driver"] = path_to_chrome_driver
#driver = webdriver.Chrome(path_to_chrome_driver, options=options)
##################################################

catlist = []

def output_print():
    return

##
# Download reviews and store them.
# 
def get_review(product_url, output_file):

    max_review_scrolls = 100

    try:

        driver.get(str(product_url))
    except:
        return

    time.sleep(1)

    # BUTTON FOR ALL REVIEWS> 
    #   class="product-reviews-opener-link Link Link--right"
    #   class berore = class="product-reviews-opener"
    while True:
        time.sleep(0.1)
        elm = "0"
        for i in range(max_review_scrolls):
            # Scroll down to last name in list
            driver.execute_script("window.scrollTo(0, window.scrollY + 400)")
            time.sleep(0.1)
            try:
                elm = driver.find_element_by_class_name('product-reviews-opener')
                time.sleep(1)
                elm.click()
            except:
                continue
        
        break
    
    print(product_url)
    return


# Check if output files can be open
def output_files_open():
    try:
        outfile = open("logs_and_input_files/input_files_for_each_server_reviews/all_zbozi.cz_reviews", 'a')
    except IOError:
        sys.stderr.write("Cannot open outfile")
        return False
    return outfile


# Check if input file can be open
def read_file_open(server_host_name):
    path = "logs_and_input_files/input_files_for_each_server_reviews/"
    path = path + server_host_name
    print(path)
    try:
        read_file = open(path, 'r')
    except IOError:
        sys.stderr.write("Cannot open readfile")
        return False
    return read_file


#Get next category from file
def get_next_page(page_file):
    return page_file.readline()


def main():

    # Get system hostname
    server_host_name = socket.gethostname()

    # Open output files
    if output_files_open() == False: sys.exit(2)  # check if files for output can be open
    output_file = output_files_open()

    if read_file_open(server_host_name) == False: sys.exit(2)  # check if files for tput can be open
    page_file = read_file_open(server_host_name) #

    for i in range(10):
        get_review(get_next_page(page_file), output_file)        


    output_file.close()
    page_file.close()
#    display.stop()

if __name__ == '__main__':
    start = time.time()
    main()
    print(time.time() - start)
