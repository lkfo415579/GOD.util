#!/bin/bash

cat $1 \
    | ~/GOD.util/moses-scripts/scripts/generic/multi-bleu.perl -lc crazy/valid.Common.en-zh.zh \
    | sed -r 's/BLEU = ([0-9.]+),.*/\1/'

