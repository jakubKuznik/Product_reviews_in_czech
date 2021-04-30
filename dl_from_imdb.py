#!/usr/bin/env python3

import sys
import os
import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from time import sleep
import time
import codecs
from pathlib import Path
import datetime

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import selenium.webdriver.firefox

class Timer:
    def __init__(self):
        self._start_time = None
    def start(self):
        self._start_time = time.perf_counter()
    def stop(self):
        self._start_time = None
    def get_time(self):
        elapsed_time = time.perf_counter() - self._start_time
        return elapsed_time

#get all files from directory and subdirectories
def get_files_from_sub_dirs(source_dir_path):
    files = []
    #r=root d=dictionary f=files
    for r, _, f in os.walk(source_dir_path):
        for file in f:
            if '.reviews.html' in file:
                files.append(os.path.join(r, file))
    return files

#get files from source dir
def get_files(source_dir_path):
    files = []
    base = (Path(source_dir_path)).iterdir()
    for file in base:
        if '.reviews.html' in str(file):
            files.append(os.path.join(source_dir_path, file))
    return files

#check if html is fully downloaded (all reviews loaded)
def is_full_downloaded(movie_id, sorting_type, file_path):
    soup = BeautifulSoup(open(file_path, encoding='utf-8'), "html.parser")
    loaded_element = soup.find("div", {'class': 'ipl-load-more--loaded-all'})
    if loaded_element == None:
        return False
    else:
        LOG_MESSAGE("{}: is fully downloaded".format(movie_id))
        return True

#get full html 
def get_page_content(browser, movie_id, sorting_type):
    url = 'https://www.imdb.com/title/{}/reviews?sort=submissionDate&dir={}&ratingFilter=0'.format(movie_id,sorting_type)
    browser.get(url)
    try:
        button_element = browser.find_element_by_class_name('ipl-load-more__button')
    except:
        try:
            correct_website = browser.find_element_by_class_name('load-more-data')
            if correct_website != None:
                content = browser.page_source
                return content 
        except:
            return None
        return None

    t = Timer()
    t.start()
    #clicking on "Load more" button, if can
    while True:
        try:
            button_element.click()
            t.start()
        except:
            try:
                #site is fully loaded
                loaded = browser.find_element_by_class_name('ipl-load-more--loaded-all')
                t.start()
                break
            except:
                sleep(0.1)
                if t.get_time() > 600:
                    return "unexpected"
                
    t.stop()
    content = browser.page_source
    return content 

#save file to dest 
def save_html(output_path, content):
    file = codecs.open(output_path, 'w', 'utf-8')
    file.write(content)
    file.close()
    return None

def LOG_MESSAGE(message):
    if not args.quite:
        print("{}\t{}".format(datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"), message))

#check if destination dictionary exists, if not dictionary will be created
def is_dest_exists(destination_dir):
    if not os.path.isdir(destination_dir):
        try:
            os.makedirs(destination_dir)
        except OSError:
            LOG_MESSAGE("Creation of the destination dictionary {} wasn't successful".format(destination_dir))
            return False

    return True

def process_files(browser, files, src_dir, des_dir):
    for file in files:
        sorting_type = os.path.basename(file).split('.')[2]
        movie_id = os.path.basename(file).split('.')[0]
        #check if site is full opened ("all reviews are show")
        if not is_full_downloaded(movie_id, sorting_type, file):

            #get content of html
            content = get_page_content(browser, movie_id, sorting_type)

            if content != None and content != "unexpected":
                #init output file
                src_ex = str(os.path.abspath(src_dir))
                dest_ex = str(os.path.abspath(file.replace(str(os.path.basename(file)), "")))
                #if src_path is differnt from dest_path, must be created correct folders
                if not src_ex == dest_ex:
                    #build new path to destination
                    output_path = file.replace(str(os.path.abspath(src_dir)), str(os.path.abspath(des_dir)))
                    output_file_name = "{}.reviews.html".format(movie_id)
                    #check if directory exists 
                    output_dir = output_path.replace(output_file_name, "")
                    if not is_dest_exists(output_dir):
                        continue

                else:
                    #build simple path to destination
                    output_destination = os.path.abspath(des_dir)
                    output_file_name = "{}.reviews.html".format(movie_id)
                    #check if directory exists
                    if not is_dest_exists(output_destination):
                        continue
                    output_path = os.path.join(output_destination, output_file_name)

                save_html(output_path, content)
            else:
                LOG_MESSAGE("{}: is fully downloaded".format(movie_id))

    return None


def init_selenium_browser():
    cap = DesiredCapabilities.CHROME
    cap['chromeOptions']  = {"args": ["--headless --ignore-certificate-errors"]}
    browser = webdriver.Remote(
            command_executor='http://{}/wd/hub'.format(selenium_server_ip), 
            desired_capabilities=cap
    )
    return browser

def init_selenium_browser_localy(path_to_chromedriver = None):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.binary_location = '/usr/bin/google-chrome'
    #chrome_options.binary_location = '/usr/bin/chromium_browser'

    path_to_chromedriver = '/usr/bin/chromedriver'
    chrome_driver = ''
    if path_to_chromedriver == None:
        chrome_driver = '/mnt/minerva1/nlp/projects/imdb_reviews/chromedriver_86'
    else:
        chrome_driver = path_to_chromedriver

    os.environ["webdriver.chrome.driver"] = chrome_driver
    browser = webdriver.Chrome(executable_path=chrome_driver, options=chrome_options)
    return browser

def process_single(browser, movie_id, des_dir, sorting_type):
    content = get_page_content(browser, movie_id, sorting_type)

    output_destination = os.path.abspath(des_dir)
    output_file_name = "{}.reviews.html".format(movie_id)
    if not is_dest_exists(output_destination):
        return
    output_path = os.path.join(output_destination, output_file_name)

    if content == None:
        LOG_MESSAGE("{}: Content is None".format(movie_id))
        return
    elif content == "unexpected":
        LOG_MESSAGE("{}: Unexpected behaviour on website, please check it".format(movie_id))
        return
    save_html(output_path, content)

    LOG_MESSAGE("{}: is fully downloaded".format(l))
    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download fully opened website (all reviews are show)')
    usage_group = parser.add_mutually_exclusive_group(required=True)
    selenium_group = parser.add_mutually_exclusive_group(required=True)

    #usage_group.add_argument('-s', '--src_dir', type=str, help='Path to source directory')
    usage_group.add_argument('-m', '--movie', type=str, help='ID of movie to download')
    usage_group.add_argument('-f', '--file_ids', type=str, help='File with ID\'s of movies to download')

    parser.add_argument('dest_dir', help='Path to destination directory')
    #parser.add_argument('-r', '--recursive', action='store_true', help='Browse subfolders and preserver a cascade of folders, destination folder is using as root')
    parser.add_argument('-q', '--quite', action='store_true', help='Without printing processed files')

    selenium_group.add_argument('-l', '--local', action='store_true', help='Run selenium localy (webdriver is in same directory as script (chromedriver_86)')
    selenium_group.add_argument('-ip', type=str, help='IP of Selenium-server-standalone')
    parser.add_argument('-c', '--chromedriver', type=str, help='Path to chromedriver')
    args = parser.parse_args()

    selenium_server_ip = args.ip

    if args.local:
        if args.chromedriver != None:
            browser = init_selenium_browser_localy(args.chromedriver)
        else:
            browser = init_selenium_browser_localy()
    else:
        browser = init_selenium_browser()

    if args.movie != None:
        if "tt" in args.movie:
            process_single(browser, args.movie, args.dest_dir, 'desc')
        else:
            process_single(browser, "tt{}".format(args.movie), args.dest_dir, 'desc')
    elif args.file_ids != None:
        f = open(args.file_ids, "r")
        for l in f:
            l = l.replace("\n", "")
            if "tt" not in l:
                l = "tt{}".format(l)

            pref_dir = ('0'+str(l)[2:])[-8:-4]
            if os.path.exists(os.path.join(args.dest_dir, pref_dir, l + ".reviews.html")):
                LOG_MESSAGE("{}: skiped".format(l))
                continue

            process_single(browser, l, os.path.join(args.dest_dir, pref_dir), 'desc')
            sleep(1)

        f.close()
    '''
    elif args.src_dir != None:
        if not args.recursive:
            files = get_files(os.path.abspath(args.src_dir))
            process_files(browser, files, args.src_dir, args.dest_dir)
        else:
            files = get_files_from_sub_dirs(os.path.abspath(args.src_dir))
            process_files(browser, files, args.src_dir, args.dest_dir)
    '''
    browser.quit()

