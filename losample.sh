#!/bin/bash

TRAIN="$1"
RATE="$2"

sort -u $TRAIN -o $TRAIN
grep 1$ ${TRAIN} | cut -d' ' -f 1 > train_pos

if [ -z "$RATE" ]
then
    RATE=$(echo "$(wc -l < ${TRAIN}) / $(wc -l < train_pos)" | bc)
    RATE=$(echo "$RATE - 1" | bc)
fi

for i in $(seq 1 $(echo "$RATE - 1" | bc))
do
    ./rotate.py train_pos --rand=$(echo "$i*3" | bc) --noBlack
    # ./rotate.py train_pos --rand=$(echo "$i*3" | bc) --noBlack | xargs -i echo {} 1 >> $TRAIN
done

rm train_pos
shuffle -i $TRAIN
