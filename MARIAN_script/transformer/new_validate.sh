#!/bin/bash

cat $1 \
    | ~/GOD.util/moses-scripts/scripts/generic/multi-bleu.perl -lc news/valid.News.en-zh.zh \
    | sed -r 's/BLEU = ([0-9.]+),.*/\1/'

