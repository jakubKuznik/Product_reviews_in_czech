#!/bin/bash
## RUN ./run_product_download.sh 
	#on all the servers stored in:
		# KNOT_SERVERS
parallel-ssh -A -h KNOT_SERVERS "/mnt/minerva1/knot/projects/product_reviews_in_czech/run_product_download.sh"

