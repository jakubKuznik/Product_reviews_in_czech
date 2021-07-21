#!/bin/bash

### ZAPNOUT PO KAZDEM SPUŠTĚNÍ PYTHON SKRIPTU NA STAHOVÁNÍ Z WEBU ZBOŽÍ.CZ
# Zalohuje logy, recenze a odkazy. Kopíruje je na správné místo a maže duplicitní zápisy

PATH_TO_PROGRAM=""  	## What log will i divide to multiple logs for each serer 
			## reviews || products_url
LINE_SUM=0		## based on that i will count how many lines should every server get 
SERVERS_SUM=62 		## How many servers are there

USERNAME="unknown"	## Username for KNOT servers
PRODUCT_START="false"	## If i would run products_url_downloader
REVIEW_START="false"	## if i would run review_downloader.py


cat /dev/null > .line_separator_start  # Clear line_separator_starter

##
# Just printi help and exit with code 0
print_help()
{

	echo "This shell script always backup logs and prepare input files for each server."
	echo "U can start zbozi.cz scape scripts using some commands."
	echo "Warning it starts downloading on all 62 KNOT serveres so it could cause some network trafic."
	echo "............................................................................................."
	echo "Usage: FINISH.sh [-h|--help] [--product_url] [-u username]"
	echo "............................................................................................."
	echo "-u username"     .... Your username for knot servers [for example xkuzni04] without that 
	echo " .................... you cannot run COMMANDS"
	echo "COMMANDS"
	echo ".. --product_url .... Run products_url_downloader.py on all KNOT servers using paralel ssh."
	echo "..................... It downloads all the product url to all_zbozi.cz_products_url.log. "
	echo "..................... NEEDS USERNAME"
	echo ".. --reviews ........ Run all_zbozi.cz_reviews.log on all KNOT servers using paralel ssh"
	echo "..................... it download product revies and store them to all_zbozi.cz_reviews.log"
	echo "..................... NEED USERNAME! (-u)"
	echo "HELP"
	echo ".. -h --help ...... Print help "
	exit 0
}

##
# Parse input arguments and COMMANDS 
argument_parser()
{
	if [ "$#" -eq "0" ];then
		return 0	
	fi
	while [ "$#" -gt 0 ]; do
		case "$1" in #COMMANDS THERE CAN BE ONLY ONE 
		#HELP###############
		-h)
			print_help
			;;
		--help)
			print_help
			;;
		--producit_url)
			PRODUCT_START="true"	## If i would run products_url_downloader
			shift; ;;
		--reviews)
			REVIEW_START="true"	## if i would run review_downloader.py
			shift; ;;
		-u)
			if [ -z "$2" ]; then
				echo "ERROR missing argument after -u" >&2 
				exit 2	
			fi
			USERNAME="$2"
			shift; shift; ;;
		*) 
			shift; ;;

		esac
	done
	echo "uuu"
}


## Divide categories to files 
divide_log_to_all_servers()
{

	FILE_INDEX=0 #FILE INDEX FROM 1 - 62

	#ATHENA 1 - 20
	for i in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20
	do
		B=$(echo "$PATH_TO_PROGRAM/line_separator $FILE_INDEX $LINE_SUM > $PATH_TO_PROGRAM/athena$i &")
		echo "$B" >> .line_separator_start 
		FILE_INDEX=$((FILE_INDEX+1))
	done
	#MINERVA 1 - 3
	for i in 1 2 3
	do
		B=$(echo "$PATH_TO_PROGRAM/line_separator $FILE_INDEX $LINE_SUM > $PATH_TO_PROGRAM/minerva$i &")
		echo "$B" >> .line_separator_start
		FILE_INDEX=$((FILE_INDEX+1))
	done
	#KNOT 01 - 09
	for i in 1 2 3 4 5 6 7 8 9 
	do
		B=$(echo "$PATH_TO_PROGRAM/line_separator $FILE_INDEX $LINE_SUM > $PATH_TO_PROGRAM/knot0$i &")
		echo "$B" >> .line_separator_start
		FILE_INDEX=$((FILE_INDEX+1))
	done
	#KNOT 10 - 36
	for i in 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39  
	do
		B=$(echo "$PATH_TO_PROGRAM/line_separator $FILE_INDEX $LINE_SUM > $PATH_TO_PROGRAM/knot$i &")
		echo "$B" >> .line_separator_start
		FILE_INDEX=$((FILE_INDEX+1))
	
	chmod u+x .line_separator_start
	done
}

categories_backup_and_store()
{
	### Delete duplicated lines and copy file: all_zbozi.cz_categories_url.log
	# backup
	cp logs_and_input_files/all_zbozi.cz_categories_url.log logs_and_input_files/backup_all_zbozi.cz_categories_url.log
	# delete duplicated lines 
	cat logs_and_input_files/all_zbozi.cz_categories_url.log | uniq -u > .help
	cat .help > logs_and_input_files/all_zbozi.cz_categories_url.log
	# copy to project root directory 
	cp logs_and_input_files/all_zbozi.cz_categories_url.log all_zbozi.cz_categories_url.log
	cp logs_and_input_files/all_zbozi.cz_categories_url.log logs_and_input_files/input_files_for_each_server_products/all_zbozi.cz_categories_url.log
}
divide_categories_set_variables()
{
	PATH_TO_PROGRAM="logs_and_input_files/input_files_for_each_server_products"
	# Count how many categories are there
	CATEGORIES_FILE="logs_and_input_files/input_files_for_each_server_products/all_zbozi.cz_categories_url.log"
	CATEGORIES_SUM=$(wc -l "$CATEGORIES_FILE" | awk '{print $1}')
	# Just count how many lines will every file contain it looks hard but just do CATEGORIES_SUM / SERVERS_SUM and store to LINE_SUM 
	LINE_SUM=`echo "$LINE_SUM" | awk -v a=$CATEGORIES_SUM -v b=$SERVERS_SUM '{result = a / b + 1}END{printf("%f",result)}' `; LINE_SUM=`printf %.0f $LINE_SUM`
}
products_backup_and_store()
{
	### Delete duplicated lines and copy file: all_zbozi.cz_products_url.log
	# backup
	cp logs_and_input_files/all_zbozi.cz_products_url.log logs_and_input_files/backup_all_zbozi.cz_products_url.log
	# delete duplicated 
	cat logs_and_input_files/all_zbozi.cz_products_url.log | uniq -u > .help
	cat .help > logs_and_input_files/all_zbozi.cz_products_url.log
	# copy to project root directory 
	cp logs_and_input_files/all_zbozi.cz_products_url.log all_zbozi.cz_products_url.log
}
divide_product_set_variables()
{
	PATH_TO_PROGRAM="logs_and_input_files/input_files_for_each_server_reviews"

	PRODUCT_FILE="logs_and_input_files/input_files_for_each_server_reviews/all_zbozi.cz_products_url.log"
	PRODUCT_URL_SUM=$(wc -l "$PRODUCT_FILE" | awk '{print $1}')
	PATH_TO_PROGRAM="logs_and_input_files/input_files_for_each_server_reviews"

	# Just count how many lines will every file contain it looks hard but just do PRODUCT_URL_SUM / SERVERS_SUM and store to LINE_SUM 
	LINE_SUM=`echo "$LINE_SUM" | awk -v a=$PRODUCT_URL_SUM -v b=$SERVERS_SUM '{result = a / b + 1}END{printf("%f",result)}' `; LINE_SUM=`printf %.0f $LINE_SUM`
}
review_backup_and_store()
{
	### Backup and copz reviews file: all_zbozi.cz_reviews.log 
	cp logs_and_input_files/all_zbozi.cz_reviews.log all_zbozi.cz_reviews.log
	cp logs_and_input_files/all_zbozi.cz_reviews.log logs_and_input_files/backup_all_zbozi.cz_reviews.log
}


argument_parser "$@" 		# Parse arguments and store them.
categories_backup_and_store
divide_categories_set_variables
divide_log_to_all_servers 	### FUNCTION GENERATE line_separator.c starter
				## Now divide categories to files for each server 
echo "Categories: $CATEGORIES_SUM"

products_backup_and_store
divide_product_set_variables
divide_log_to_all_servers 	### FUNCTION GENERATE line_separator.c starter
				## Now divide product_url to files for each server 

echo "Products URL: $PRODUCT_URL_SUM"

./.line_separator_start &       ## Start dividing logs to file for each server.
				# generated bz divide_log_to_all_servers file

review_backup_and_store



