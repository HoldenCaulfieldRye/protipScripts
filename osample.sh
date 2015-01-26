#!/bin/bash

TRAIN="$1"
RATE="$2"

sort -u $TRAIN -o $TRAIN
grep 1$ ${TRAIN} > train_pos

if [ -z "$RATE" ]
then
    RATE=$(echo "$(wc -l < ${TRAIN}) / $(wc -l < train_pos)" | bc)
    RATE=$(echo "$RATE - 1" | bc)
fi

for i in $(seq 1 $(echo "$RATE - 1" | bc))
do
    cat train_pos >> $TRAIN
done
rm train_pos
shuffle -i $TRAIN
