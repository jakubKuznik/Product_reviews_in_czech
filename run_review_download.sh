#!/bin/bash
#RUN products_url_donloader.py in tmux so it doesnt end with ssh 
cd /mnt/minerva1/knot/projects/product_reviews_in_czech
tmux new-session -d -s mySession -n myWindow

tmux send-keys -t mySession:myWindow "cd /mnt/minerva1/knot/projects/product_reviews_in_czech" Enter
tmux send-keys -t mySession:myWindow "python3 review_downloader.py >log 2>log_err &" Enter

exit
