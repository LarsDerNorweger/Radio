#!/bin/bash

cd ~/Radio/Internal
read P < ./PID.txt
kill $P
echo "[$(date)] Process $P killed and restarted" >> ../Restart.log
python3 ../main.py

