#!/bin/bash

SRCL=en
TGTL=zh
TERM=Medicine
VALID=brave/1600.medicine.raw.$TGTL

cat $1 | sed 's/@@ //g' | python ~/GOD.util/util_token/detokenize.py -l zh -m \
    | sacrebleu $VALID \
    | sed -r 's/.*\.7 = ([0-9.]+) .*/\1/'
