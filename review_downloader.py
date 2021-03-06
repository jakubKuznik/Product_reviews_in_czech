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

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains

from bs4 import BeautifulSoup

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
path_to_chromedriver = '/mnt/minerva1/knot/projects/product_reviews_in_czech/drivers/chromedriver'
chrome_driver = '/mnt/minerva1/nlp/projects/imdb_reviews/chromedriver_86'
path_to_chrome_driver = 'drivers/chromedriver'
os.environ["webdriver.chrome.driver"] = path_to_chrome_driver
driver = webdriver.Chrome(path_to_chrome_driver, options=options)
##################################################


##
# Format rewievs and print them to output file
# @soup all reviews of given page
# @product_url url of page that reviews are from
#          - "author" - jm??no autora
#          - "date" - datum vytvo??en?? p????sp??vku
#          - "rating" - hodnocen?? produktu v %
#          - "pros" - seznam v??ech klad?? produktu
#          - "cons" - seznam v??ech z??por?? produktu
#          - "summary" - voln?? text vyj??d??en?? recenzenta k produktu
#          - "usefulness_of_review" - u??ite??nost recenze z pohledu ostatn??ch recenzent?? ozna??en?? palci nahoru nebo dol??
def format_output(soup, product_url, product_name):
    obj_product = {}
    obj_reviews = []
    
    
    reviews = soup.find_all(class_="ProductReviewsItem experience")
    time.sleep(1)
    for rev in reviews:
        author = get_autor(rev)      # find author
        date = get_date(rev)         # findout date that review was writen    
        rating = get_rating(rev)     # find rating in percent
        pros = get_pros(rev)         # find positive information
        cons = get_cons(rev)         # find negative information
        summary = get_summary(rev)   # find product review summary
        ussefulness = get_ussefulness(rev) 
        
        #serazena verze objektu recenze
        obj_rev = {"review":OrderedDict([("author",author),("date",date),("rating",rating),("pros",pros),("cons",cons),("summary",summary),("usefulness_of_review",ussefulness)])}
        #vlozi do seznamu vsech recenzi k aktualnimu produktu
        obj_reviews.append(obj_rev)

    obj_product[product_name] = obj_reviews
    #print(obj_product)
    return obj_product


##
# positive - class="ProductReviewsItem-footer-voting-button ProductReviewsItem-footer-voting-button--like"
# negative - class="ProductReviewsItem-footer-voting-button ProductReviewsItem-footer-voting-button--dislike"
def get_ussefulness(rev):
    ussefulness = []
    
    yes = "ANO "
    try:
        yes_int = rev.find(class_="ProductReviewsItem-footer-voting-button ProductReviewsItem-footer-voting-button--like")
        yes_int = yes_int.get_text().lstrip()
        yes_int = yes_int.rstrip()
    except:
        yes_int = "null"

    no = "NO "
    try:
        no_int = rev.find(class_="ProductReviewsItem-footer-voting-button ProductReviewsItem-footer-voting-button--dislike")
        no_int = no_int.get_text().lstrip()
        no_int = no_int.rstrip()
    except:
        no_int = "null"


    yes = yes + yes_int
    no = no + no_int

    ussefulness = [yes, no]
    return ussefulness


##
# class="ProductReviewsItem-experience ProductReviewsItem-experience--overall"
def get_summary(rev):
    summary = ""
    try:
        summary = rev.find(class_="ProductReviewsItem-experience ProductReviewsItem-experience--overall")
        sum = summary.get_text().lstrip()
        sum = sum.rstrip()
    except:
        return ""
   # print("SUM ",summary)

    return sum

##
# class="ProductReviewsItem-experience ProductReviewsItem-experience--negative"
def get_cons(rev):
    cons = ""
    try:
        cons = rev.find(class_="ProductReviewsItem-experience ProductReviewsItem-experience--negative")
        cons = cons.get_text().lstrip()
        cons = cons.rstrip()
    except:
        return ""
    #print("CONS",cons)
    return cons

##
# class="ProductReviewsItem-experience ProductReviewsItem-experience--positive"
def get_pros(rev):
    pros = ""
    try:
        pros = rev.find(class_="ProductReviewsItem-experience ProductReviewsItem-experience--positive")
        pros = pros.get_text().lstrip()
        pros = pros.rstrip()
    except:
        return ""
    #print("PROS", pros)
    return pros


## 
# Extract date
# class="ProductReviewsItem-header-date"
#
def get_date(rev):
    try:
        date = rev.find(class_="ProductReviewsItem-header-date")
        date = date.get_text().lstrip()
        date = date.rstrip()
    except:
        date = "null"
    return date

## 
# Get autor name.
# class="ProductReviewsItem-header-user"
#
def get_autor(rev):
    try:
        author = rev.find(class_="ProductReviewsItem-header-user")
        aut = author.get_text().lstrip()
        aut = aut.rstrip()
        aut = aut.replace("Ov????en?? n??kup", "")
    except:
        aut = "null"
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
    soup = BeautifulSoup(infile, "html.parser")
    
    reviews_sum = soup.find(class_="ProductRating-rating-count")
    print("GGGGG",reviews_sum)

    return reviews_sum

##
# Get product name from whole soup 
# class_="Breadcrumbs-title"
def get_product_name(soup):
    try:
        product_name = soup.find(class_="Breadcrumbs-title")   
        product_name = product_name.get_text().lstrip()
        product_name = product_name.rstrip()
    except:    
        product_name = "unknown"
    return product_name
       
##
# Download reviews and store them.
# 
def get_review(product_url, output_file):
    
    time.sleep(0.5)
    try:
        driver.get(str(product_url))
    except:
        return
    
    time.sleep(0.5)
    
    ## TODO MAX REVIEW SCROLL FROM NUMBER OF REVIEWS 
    # max_review_scrolls = 100
    max_review_scrolls = 20
    
    time.sleep(0.1)
    elm = "0"
    
    # LOAD ALL REVIEWS
    for i in range(max_review_scrolls):
        # Scroll down to last name in list
        driver.execute_script("window.scrollTo(0, window.scrollY + 400)")
        time.sleep(0.1)
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
    soup = BeautifulSoup(infile, "html.parser")
    time.sleep(2)
    
    soup2 = soup

    product_name = get_product_name(soup2)
    if product_name == "unknown":
        return 0
    ## Get all the reviews information and print them to output 
    return format_output(soup, product_url, product_name)



##
#  Check if output files can be open
def output_files_open():
    try:
        outfile = open("logs_and_input_files/all_zbozi.cz_reviews.log", 'a')
    except IOError:
        sys.stderr.write("Cannot open outfile")
        return False
    return outfile


##
#  Check if input file can be open
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

##
#  count lines in given file 
def get_file_lines(file):
    path = "logs_and_input_files/input_files_for_each_server_reviews/"
    path = path + file
    file = open(path, "r")
    line_count = 0
    for line in file:
        if line != "\n":
            line_count += 1
    file.close()        
    return line_count


##
#  Get next category from file
def get_next_page(page_file):
    return page_file.readline()

## 
# Parse arguments
def parse_args():
        
        parser = argparse.ArgumentParser(description='KNOT - product reviews in czech - Author: Jakub Kuzn??k {xkuzni04} \
        ', add_help=False)
        parser.add_argument("-h", "--help", action="count", default=0, help="tisk napovedy")
        
        try:
                args = parser.parse_args()
        except:
                sys.exit(1)

        if(args.help == 1):
                if(len(sys.argv) == 2):
                        parser.print_help()
                        print("\n\nProgram otev??e vstupn?? soubor kter?? je stejn?? jako hostname serveru logs_and_input_files/input_files_for_each_server_reviews/hostname\nPostupn?? za??ne ukl??dat ve??ker?? url jednotliv??ch produkt?? do souboru logs_and_input_files/all_zbozi.cz_reviews.log \n")
                        sys.exit(0)
                else:
                        print("Error: Help with other argument", file=sys.stderr)
                        sys.exit(1)

        return args




def main():


    parse_args()


    server_host_name = socket.gethostname() # Get system hostname

    products_sum = get_file_lines(server_host_name)

    # Open output files
    if output_files_open() == False: sys.exit(2)  # check if files for output can be open
    output_file = output_files_open()

    if read_file_open(server_host_name) == False: sys.exit(2)  # check if files for tput can be open
    page_file = read_file_open(server_host_name) #

    all_product = []    # all product with reviews 
    for i in range(products_sum):
        rewiev = get_review(get_next_page(page_file), output_file)
        if rewiev == 0:
            continue
        all_product.append(rewiev)

    #uprava koncoveho objektu
    final_JSON = {}
    final_JSON["REVIEWS"] = all_product
    json_out = json.dumps(final_JSON, indent=4, ensure_ascii=False)  #formatovani koncoveho objektu
    output_file.write(json_out)
    print(json_out)

    output_file.close()
    page_file.close()
    driver.close()
#    display.stop()


if __name__ == '__main__':
    start = time.time()
    main()
    print(time.time() - start)
