#!/bin/sh
SCRIPT_DIR=`dirname $0`
cd $SCRIPT_DIR

echo -n $1 | base64 > p
