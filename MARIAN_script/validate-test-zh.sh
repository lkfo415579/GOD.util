#!/bin/bash

cat $1 \
    | sed 's/@@ //g' \
    | python ~/GOD.util/util_token/detokenize.py -l zh \
    | python -m jieba -d 2> /dev/null \
    | sed 's/  / /g' | sed 's/  / /g' \
    | ~/GOD.util/moses-scripts/scripts/generic/multi-bleu.perl -lc $2 \
    | sed -r 's/BLEU = ([0-9.]+),.*/\1/'

