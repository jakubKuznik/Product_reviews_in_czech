#! /bin/sh

#./line_separator 10 11702 > athena8
#/home/shadov/Desktop/VUT/1bit/2.letni/KNOT/product_reviews_in_czech/logs_and_input_files/input_files_for_each_server_reviews

PATH_TO_PROGRAM="/home/shadov/Desktop/VUT/1bit/2.letni/KNOT/product_reviews_in_czech/logs_and_input_files/input_files_for_each_server_reviews"
A=0 #FILE INDEX FROM 1 - 62

#ATHENA 1 - 20
for i in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20
do
	B=$(echo "$PATH_TO_PROGRAM/line_separator $A 11702 > athena$i &")
	echo "$B"
	A=$((A+1))
done
#MINERVA 1 - 3
for i in 1 2 3
do
	B=$(echo "$PATH_TO_PROGRAM/line_separator $A 11702 > minerva$i &")
	echo "$B"
	A=$((A+1))

done
#KNOT 01 - 09
for i in 1 2 3 4 5 6 7 8 9 
do
	B=$(echo "$PATH_TO_PROGRAM/line_separator $A 11702 > knot0$i &")
	echo "$B"
	A=$((A+1))

done
#KNOT 10 - 36
for i in 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39  
do
	B=$(echo "$PATH_TO_PROGRAM/line_separator $A 11702 > knot$i &")
	echo "$B"
	A=$((A+1))

done

