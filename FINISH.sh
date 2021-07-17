#!/bin/bash

### ZAPNOUT PO KAZDEM SPUŠTĚNÍ PYTHON SKRIPTU NA STAHOVÁNÍ Z WEBU ZBOŽÍ.CZ
# Zalohuje logy, recenze a odkazy. Kopíruje je na správné místo a maže duplicitní zápisy

PATH_TO_PROGRAM=""  	## What log will i divide to multiple logs for each serer 
			## reviews || products_url
LINE_SUM=0		## based on that i will count how many lines should every server get 
SERVERS_SUM=62 		## How many servers are there

 
## Divide categories to files 
divide_log_to_all_servers()
{

	FILE_INDEX=0 #FILE INDEX FROM 1 - 62

	#ATHENA 1 - 20
	for i in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20
	do
		B=$(echo "$PATH_TO_PROGRAM/line_separator $FILE_INDEX $LINE_SUM > athena$i &")
		echo "$B"
		FILE_INDEX=$((FILE_INDEX+1))
	done
	#MINERVA 1 - 3
	for i in 1 2 3
	do
		B=$(echo "$PATH_TO_PROGRAM/line_separator $FILE_INDEX $LINE_SUM > minerva$i &")
		echo "$B"
		FILE_INDEX=$((FILE_INDEX+1))
	done
	#KNOT 01 - 09
	for i in 1 2 3 4 5 6 7 8 9 
	do
		B=$(echo "$PATH_TO_PROGRAM/line_separator $FILE_INDEX $LINE_SUM > knot0$i &")
		echo "$B"
		FILE_INDEX=$((FILE_INDEX+1))
	done
	#KNOT 10 - 36
	for i in 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39  
	do
		B=$(echo "$PATH_TO_PROGRAM/line_separator $FILE_INDEX $LINE_SUM > knot$i &")
		echo "$B"
		A=$((A+1))
	done
}


### Delete duplicated lines and copy file: all_zbozi.cz_categories_url.log
# backup
cp logs_and_input_files/all_zbozi.cz_categories_url.log logs_and_input_files/backup_all_zbozi.cz_categories_url.log
# delete duplicated lines 
cat logs_and_input_files/all_zbozi.cz_categories_url.log | uniq -u > .help
cat .help > logs_and_input_files/all_zbozi.cz_categories_url.log
# copy to project root directory 
cp logs_and_input_files/all_zbozi.cz_categories_url.log all_zbozi.cz_categories_url.log
cp logs_and_input_files/all_zbozi.cz_categories_url.log logs_and_input_files/input_files_for_each_server_products/all_zbozi.cz_categories_url.log

# Count how many categories are there
CATEGORIES_FILE="logs_and_input_files/input_files_for_each_server_products/all_zbozi.cz_categories_url.log"
CATEGORIES_SUM=$(wc -l "$CATEGORIES_FILE" | awk '{print $1}')
echo "Categories: $CATEGORIES_SUM"
PATH_TO_PROGRAM="/home/shadov/Desktop/VUT/1bit/2.letni/KNOT/product_reviews_in_czech/logs_and_input_files/input_files_for_each_server_products"

LINE_SUM=`echo "$LINE_SUM" | awk -v a=$CATEGORIES_SUM -v b=$SERVERS_SUM '{result = a / b + 1}END{printf("%f",result)}' `; LINE_SUM=`printf %.0f $LINE_SUM`
#SUM1=`echo "$SUM1" | awk -v s=$SUM1 '{v = s - 0.5}END{printf("%f", v)}'`;SUM1=`printf %.0f $SUM1`

divide_log_to_all_servers ### FUNCTION GENERATE line_separator.c starter


### Delete duplicated lines and copy file: all_zbozi.cz_products_url.log
# backup
cp logs_and_input_files/all_zbozi.cz_products_url.log logs_and_input_files/backup_all_zbozi.cz_products_url.log
# delete duplicated 
cat logs_and_input_files/all_zbozi.cz_products_url.log | uniq -u > .help
cat .help > logs_and_input_files/all_zbozi.cz_products_url.log
# copy to project root directory 
cp logs_and_input_files/all_zbozi.cz_products_url.log all_zbozi.cz_products_url.log
PATH_TO_PROGRAM="/home/shadov/Desktop/VUT/1bit/2.letni/KNOT/product_reviews_in_czech/logs_and_input_files/input_files_for_each_server_reviews"



### Backup and copz reviews file: all_zbozi.cz_reviews.log 
cp logs_and_input_files/all_zbozi.cz_reviews.log all_zbozi.cz_reviews.log
cp logs_and_input_files/all_zbozi.cz_reviews.log logs_and_input_files/backup_all_zbozi.cz_reviews.log



