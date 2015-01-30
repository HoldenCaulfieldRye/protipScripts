#!/bin/bash

FNAME=$1
NAME=$FNAME
i=2
while [ -e $NAME ]
do
    NAME=${FNAME}_${i}
    i=$(echo "$i + 1" | bc)
done
    
echo $NAME
