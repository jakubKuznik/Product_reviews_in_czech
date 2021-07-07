#!/bin/bash

### ZAPNOUT PO KAZDEM SPUŠTĚNÍ PYTHON SKRIPTU NA STAHOVÁNÍ Z WEBU ZBOŽÍ.CZ
# Zalohuje logy, recenze a odkazy. Kopíruje je na správné místo a maže duplicitní zápisy


### Delete duplicated lines and copy file: all_zbozi.cz_categories_url.log
# backup
cp logs_and_input_files/all_zbozi.cz_categories_url.log logs_and_input_files/backup_all_zbozi.cz_categories_url.log
# delete duplicated 
cat logs_and_input_files/all_zbozi.cz_categories_url.log | uniq -u > .help
cat .help > logs_and_input_files/all_zbozi.cz_categories_url.log
# copy to project root directory 
cp logs_and_input_files/all_zbozi.cz_categories_url.log all_zbozi.cz_categories_url.log


### Delete duplicated lines and copy file: all_zbozi.cz_products_url.log
# backup
cp logs_and_input_files/all_zbozi.cz_products_url.log logs_and_input_files/backup_all_zbozi.cz_products_url.log
# delete duplicated 
cat logs_and_input_files/all_zbozi.cz_products_url.log | uniq -u > .help
cat .help > logs_and_input_files/all_zbozi.cz_products_url.log
# copy to project root directory 
cp logs_and_input_files/all_zbozi.cz_products_url.log all_zbozi.cz_products_url.log


### Backup and copz reviews file: all_zbozi.cz_reviews.log 
cp logs_and_input_files/all_zbozi.cz_reviews.log all_zbozi.cz_reviews.log
cp logs_and_input_files/all_zbozi.cz_reviews.log logs_and_input_files/backup_all_zbozi.cz_reviews.log




