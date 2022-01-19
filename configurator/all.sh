#!/bin/bash

set -e # Выход при обнаружении ошибки

PROGDIR=$(dirname $0)
cd $PROGDIR

f=`ls -1 | grep '^step.*\.py' | sort`

for file in $f
do

 echo "------------------------------------------------------------------------"
 echo "Processing ${file}"
 echo "------------------------------------------------------------------------"
 echo ""

 /usr/bin/python3 ./${file}

done 
