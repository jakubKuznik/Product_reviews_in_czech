# Upravil
# Kuznik Jakub
# KNOT - product_reviews_in_czech
# xkuzni04@stud.fit.vutbr.cz
# This script should get all the zbozi.cz urls
# xkuzni04@stud.fit.vutbr.cz



#This script should get through all the categories and get all the subcategories from web zbozi.cz
#It is being developed and it is not tested yet.
#Output will go to file> all_zbozi.cz_products_url
#Using selenium and chromedriver
#Google chrome version Version 88.0.4324.182

import time
import sys
from typing import List, Any

import argparse

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from pyvirtualdisplay import Display

display = Display(visible=0, size=(800, 600))
display.start()
options = Options()
options.binary_location = "/usr/bin/google-chrome"    #chrome binary location specified here
#options.add_argument('--headless')
#options.add_argument("--start-maximized") #open Browser in maximized mode
options.add_argument("--no-sandbox") #bypass OS security model
options.add_argument("--disable-dev-shm-usage") #overcome limited resource problems
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome('drivers/chromedriver', options=options)

# RUN ON MINERVA - CHROME MODE
#options = Options()
#options.add_argument('--headless')
#options.add_argument('--no-sandbox')
#options.add_argument('--disable-dev-shm-usage')
#options.binary_location = '/usr/bin/google-chrome'
#path_to_chromedriver = '/usr/bin/chromedriver'
#chrome_driver = '/mnt/minerva1/nlp/projects/imdb_reviews/chromedriver_86'
#path_to_chrome_driver = 'drivers/chromedriver'
#os.environ["webdriver.chrome.driver"] = path_to_chrome_driver
#driver = webdriver.Chrome(path_to_chrome_driver, options=options)


category_indicator = []  # every url ll be checked if i was looking in
catlist = []




# Recursive function that should get all the pages
def get_sub_category_urls(category):

    try:
        driver.get(str(category))
    except:
        return

    time.sleep(1)
    page = driver.find_elements_by_xpath("//a[@href]")
    for elem in page:
        filter_elem = elem.get_attribute("href")
        if filter_elem not in catlist:    #if i dont have url yet
            if "#" in str(filter_elem):
                continue
            if str(category) in str(filter_elem): # if the url goes forward in categories
                if '?' not in str(filter_elem):  # if url does not contain ? it indicate urls that are not categories
                    print(filter_elem)
                    catlist.append(filter_elem)
                    category_indicator[catlist.index(filter_elem)] = False


# Gets throught url and store all subcategory urls.
# Return links that can be appended to
def open_category(url):
    sub_urls = []
    driver.get(str(url))
    page = driver.page_source
    elems = driver.find_elements_by_xpath("//a[@href]")

    for elem in elems:
        filter_elem = elem.get_attribute("href")
        sub_urls.append(filter_elem)

    return sub_urls


# Check if output files can be open
# return false if not
def output_files_open():
    try:
        outfile = open("logs_and_input_files/all_zbozi.cz_categories_url.log", 'a')
    except IOError:
        print("nelze otevrit outfile", file=sys.stderr)
        return False
    return outfile


# Ve ll need just url that contains word "vyrobek"
def filter_urls(urls, substring):
    out = []
    for url in urls:
        if substring in url:
            out.append(url)

    return out
## 
# Parse arguments
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
                        print("\n\nProgram stáhne veškere kategorie z webu zboží.cz\nVýstupní soubor: logs_and_input_files/all_zbozi.cz_categories_url.log\n")
                        sys.exit(0)
                else:
                        print("Error: Help with other argument", file=sys.stderr)
                        sys.exit(1)

        return args



def main():
    # Open output files
    parse_args()
    if output_files_open() == False: sys.exit(2)  # check if files for output can be open
    output_file = output_files_open()

    all_categories_url = ["https://www.zbozi.cz/dum-byt-a-zahrada/",
                            "https://www.zbozi.cz/domaci-spotrebice/",
                              "https://www.zbozi.cz/elektronika/",
                              "https://www.zbozi.cz/kultura-a-zabava/",
                              "https://www.zbozi.cz/sport/",
                               "https://www.zbozi.cz/telefony-navigace/",
                              "https://www.zbozi.cz/auto-moto/",
                              "https://www.zbozi.cz/detske-zbozi/",
                              "https://www.zbozi.cz/kosmetika-a-drogerie/",
                              "https://www.zbozi.cz/pocitace/",
                              "https://www.zbozi.cz/obleceni-a-moda/",
                              "https://www.zbozi.cz/zdravi/",
                              "https://www.zbozi.cz/foto/",
                              "https://www.zbozi.cz/potraviny-a-napoje/",
                              "https://www.zbozi.cz/kancelar/",
                              "https://www.zbozi.cz/eroticke-zbozi-a-pomucky/"]

    for i in range(100000000):
        category_indicator.append(False)

    for category in all_categories_url:
        get_sub_category_urls(category)
        catlist.append(category)
        category_indicator[catlist.index(category)] = True

    append = True
    while append == True:
        append = False
        for link in catlist:
            if(category_indicator[catlist.index(link)] == False):
                append = True
                get_sub_category_urls(link)
                category_indicator[catlist.index(link)] = True
            else:
                continue


    for item in catlist:
        output_file.write("%s\n" % item)
    driver.close()
    display.stop()

if __name__ == '__main__':
    start = time.time()
    main()
    print(time.time() - start)
