#!/bin/bash

logFile=../Restart.log

cd ~/Radio/Internal

echo >> $logFile
echo "System Restarted" >> $logFile
echo >> $logFile
echo "[$(date)] inital Process Started" >> $logFile

python3 ../main.py