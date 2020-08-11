#!/bin/sh
SCRIPT_DIR=`dirname $0`
cd $SCRIPT_DIR

echo "30 7 * * *" `which python3` `pwd`/main.py ">>" `pwd`/log.log "2>&1" > report.conf
