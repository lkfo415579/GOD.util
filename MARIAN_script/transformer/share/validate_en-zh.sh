#!/bin/bash

cat $1 \
    | ~/GOD.util/moses-scripts/scripts/generic/multi-bleu.perl -lc en-zh/valid.News.en-zh.en \
    | sed -r 's/BLEU = ([0-9.]+),.*/\1/'

