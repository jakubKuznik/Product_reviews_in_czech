# Kuznik Jakub
# KNOT - product_reviews_in_czech
# xkuzni04@stud.fit.vutbr.cz
# This script should get all the zbozi.cz reviews 
# xkuzni04@stud.fit.vutbr.cz

# Every server gets throught urls in 
# logs_and_input_files/input_files_for_each_server/

from collections import OrderedDict
from datetime import date, timedelta
import re

import requests
import time
import socket
import sys
import os
from typing import List, Any
from urllib.request import urlopen

sys.path.insert(0, '.')

import collections
orderedDict = collections.OrderedDict()
from collections import OrderedDict

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains

from bs4 import BeautifulSoup

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



##
# Format rewievs and print them to output file
# @soup all reviews of given page
# @product_url url of page that reviews are from
#          - "author" - jméno autora
#          - "date" - datum vytvoření příspěvku
#          - "rating" - hodnocení produktu v %
#          - "pros" - seznam všech kladů produktu
#          - "cons" - seznam všech záporů produktu
#          - "summary" - volný text vyjádření recenzenta k produktu
#          - "usefulness_of_review" - užitečnost recenze z pohledu ostatních recenzentů označená palci nahoru nebo dolů
def format_output(soup, product_url):
    #print(soup)        
    reviews = soup.find_all(class_="ProductReviewsItem experience")
    for rev in reviews:
        author = get_autor(rev)      # find author
        date = get_date(rev)         # findout date that review was writen    
        rating = get_rating(rev)     # find rating in percent
        pros = get_pros(rev)
        cons = get_cons(rev)
        summary = get_summary(rev) 
        
        #najde obsah prispevku
        #text = rev.find(class_="ProductReviewsItem-main-content")     
        print(author, date, rating)


    print(product_url)
    return
##
# class="ProductReviewsItem-experience ProductReviewsItem-experience--overall"
def get_summary(rev):
    summary = ""
    summary = rev.find(class_="ProductReviewsItem-experience ProductReviewsItem-experience--overall")
    summary = summary.get_text().lstrip()
    summary = summary.rstrip()
    print("SUM ",summary)

    return summary

##
# class="ProductReviewsItem-experience ProductReviewsItem-experience--negative"
def get_cons(rev):
    cons = ""
    cons = rev.find(class_="ProductReviewsItem-experience ProductReviewsItem-experience--negative")
    cons = cons.get_text().lstrip()
    cons = cons.rstrip()
    print("CONS",cons)
    return cons

##
# class="ProductReviewsItem-experience ProductReviewsItem-experience--positive"
def get_pros(rev):
    pros = ""
    pros = rev.find(class_="ProductReviewsItem-experience ProductReviewsItem-experience--positive")
    pros = pros.get_text().lstrip()
    pros = pros.rstrip()
    print("PROS", pros)
    return pros


## 
# Extract date
# class="ProductReviewsItem-header-date"
#
def get_date(rev):
        date = rev.find(class_="ProductReviewsItem-header-date")
        date = date.get_text().lstrip()
        date = date.rstrip()
        return date

## 
# Get autor name.
# class="ProductReviewsItem-header-user"
#
def get_autor(rev):
        author = rev.find(class_="ProductReviewsItem-header-user")
        aut = author.get_text().lstrip()
        aut = aut.rstrip()
        aut = aut.replace("Ověřený nákup", "")
        return aut



## 
# Get raiting that is represented by stars. Stars are represented 
# as percentage 4/5 stars are 80% etc.
# class="Stars-goldWrap"
#
def get_rating(rev):
        rating = ""
        rating = rev.find(class_="Stars-goldWrap")
        str_rating = str(rating)
        index = str_rating.find('width: ')

        number = ""
        for x in range(0, 4):
                if str_rating[index+x+7] == '%':
                        number+= '%'
                        break
                number+= str_rating[index+x+7]
        
        return number



##
# Find out number of reviews 
# class="ProductRating-rating-count"
def count_reviews(driver):
    
    infile = ""
    try:
        infile = driver.page_source
    except IOError:
        print("Error: Adresa nelze otevrit", file=sys.stderr)

    time.sleep(3)
    soup = BeautifulSoup(infile)
    
    reviews_sum = soup.find(class_="ProductRating-rating-count")
    print("GGGGG",reviews_sum)

    return reviews_sum


##
# Download reviews and store them.
# 
def get_review(product_url, output_file):
    
    time.sleep(0.5)
    try:
        driver.get(str(product_url))
    except:
        return
    
    ## TODO MAX REVIEW SCROLL FROM NUMBER OF REVIEWS 
    # max_review_scrolls = 100
    max_review_scrolls = 10
    
    time.sleep(0.05)
    elm = "0"
    
    # LOAD ALL REVIEWS
    for i in range(max_review_scrolls):
        # Scroll down to last name in list
        driver.execute_script("window.scrollTo(0, window.scrollY + 400)")
        time.sleep(0.05)
        try:
                elm = driver.find_element_by_class_name('product-reviews-opener')
                time.sleep(1)
                elm.click()
        except:
            break

    infile = ""
    try:
        infile = driver.page_source
    except IOError:
        print("Error: Adresa nelze otevrit", file=sys.stderr)

    time.sleep(5)
    soup = BeautifulSoup(infile)
    ## Get all the reviews information and print them to output 
    format_output(soup, product_url)

    return



# Check if output files can be open
def output_files_open():
    try:
        outfile = open("logs_and_input_files/all_zbozi.cz_reviews", 'a')
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

    server_host_name = socket.gethostname()
    # Get system hostname

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
