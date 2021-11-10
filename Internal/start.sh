#!/bin/bash

logFile=../Restart.log

echo >> $logFile
echo "System Restarted" >> $logFile
echo >> $logFile
echo "[$(date)] inital Process Started" >> $logFile

python3 ./InternalOperation.py