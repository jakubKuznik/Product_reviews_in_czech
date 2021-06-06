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
from urllib.request import urlopen

import pandas as pd

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



def formate_text(review_list, obj_reviews, actualization = False, latest_date = None, latest_author = None):
        reviews = review_list.find_all(class_="ProductReviewsItem experience")
        print(reviews)

'''
        #projde kazdy prispevek
        for rev in reviews:
                #najde informace o autorovi prispevku
                author = rev.find(class_="user")
                #najde obsah prispevku
                text = rev.find(class_="revtext")

                #odstrani fotku a nezadouci text "novacek" pod ni
                if author.find(class_="userfoto"):
                        author.find(class_="userfoto").clear()

                #odtrhne bile znaky zleva a zprava jmena autora
                aut = author.p.get_text().lstrip()
                aut = aut.rstrip()

                #datum pridani prispevku
                datee = author.find(class_="date").get_text().replace("Přidáno: ", "")
                #nahrazeni escape znaku mezerami
                datee = datee.replace('\xa0', ' ')

                #prevod data na jednotny format
                #heureka pouziva "včera" - kdyz byl prispevek pridan vcera
                #                                "před"  - kdyz byl prispevek pridan pred nekolika hodinami
                if "včera" in datee:
                        datee = (date.today() - timedelta(1)).strftime("%d. %B %Y").lstrip("0")
                        datee = date_translate(datee)

                if "před" in datee:
                        datee = date.today().strftime("%d. %B %Y").lstrip("0")
                        datee = date_translate(datee)
#pokud provadim aktualizaci, je nutno kontrolovat kazdy prispevek, zda-li je jeho datum a autor jiny nez ten od posledniho stazeni
                if actualization:
                        #pokud se tedy narazi na shodu, vraci se vse co se doposud stahlo
                        if((datee == latest_date) & (aut == latest_author)):
                                #vraci se taky True, protoze stahovani bylo zastaveno 
                                return (obj_reviews, True)

                #hodnoceni produktu
                rating = text.find(class_="hidden")
                #orezani textu a zanechani pouze procentualni hodnoty
                if rating:
                        rating = rating.get_text().replace("Hodnocení produktu: ", "")

                #doporuceni produktu
                recommends = None

                recommend_yes = text.find(class_="recommend-yes")
                if recommend_yes:
                        recommends = "YES"

                recommend_no = text.find(class_="recommend-no")
                if recommend_no:
                        recommends = "NO"

                #klady
                plus = text.find(class_="plus")
                pros = []
                if plus:
                        if plus.ul:
                                #projde elementy tabulky a kazdy vlozi do seznamu
                                for child in plus.ul.children:
                                        pros.append(child.get_text())

                #zapory
                minus = text.find(class_="minus")
                cons = []
                if minus:
                        if minus.ul:
                                for child in minus.ul.children:
                                        cons.append(child.get_text())
#shrnuti
                summary = None
                if text.p:
                        summary = text.p.get_text()

                #dotaznik
                questionnaire = None
                questions = text.find(class_="individualQuestions")
                if questions:
                        answer = False
                        a = questions.find_all('td')
                        #projde seznam a z kazde polozky vytahne jen text
                        for i in range(len(a)):
                                a[i] = a[i].get_text()
                        #ze seznamu vytvori slovnik - Otazka : Odpoved
                        #questionnaire = {a[i]:a[i+1] for i in range(0, len(a), 2)}
                        #serazena verze otazek a odpovedi
                        questionnaire = OrderedDict([(a[i],a[i+1]) for i in range(0, len(a), 2)])

                #sumarizace uzitecnosti prispevku
                evalreview = text.find(class_="evalreview")
                usefulness = None
                if evalreview:
                        usefulness = evalreview.get_text()
                        evallist = evalreview.find_all('li')
                        evallist.pop(0)
                        for i in range(len(evallist)):
                                evallist[i] = evallist[i].get_text()


                #serazena verze objektu recenze
                obj_rev = {"review":OrderedDict([("author",aut),("date",datee),("rating",rating),("recommends",recommends),("pros",pros),("cons",cons),("summary",summary),("questionnaire",questionnaire),("usefulness_of_review",evallist)])}

                #vlozi do seznamu vsech recenzi k aktualnimu produktu
                obj_reviews.append(obj_rev)

        return (obj_reviews, False)

'''









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

    
    time.sleep(0.05)
    elm = "0"
    ## LOAD ALL REVIEWS
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

    ### scrap with beautifull soup
    #     

    infile = ""
    try:
        #infile = BeautifulSoup(urlopen(product_url))
        infile = driver.page_source
    except IOError:
        print("Error: Adresa nelze otevrit", file=sys.stderr)

    time.sleep(5)
    print("BS", infile)

    print(product_url)
    return
'''
    aut = "."
    datee = "."
    rating = "."
    recommends = "."
    pros = "."
    cons = "."
    summary = "."
    questionnaire = "."
    evallist = "."
    

    #review_list = infile.find(class_="ProductReviewsItem-innerContainer ProductReviewsItem--experience")
    obj_rev = {"review":OrderedDict([("author",aut),("date",datee),("rating",rating),("recommends",recommends),\
            ("pros",pros),("cons",cons),("summary",summary),("questionnaire",questionnaire),("usefulness_of_review",evallist)])}

'''    




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
