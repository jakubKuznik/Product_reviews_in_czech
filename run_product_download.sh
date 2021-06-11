#!/bin/bash
tmux new-session -d -s mySession -n myWindow
tmux send-keys -t mySession:myWindow "python3 products_url_downloader.py 88 >log 2>log_err &" Enter
exit
