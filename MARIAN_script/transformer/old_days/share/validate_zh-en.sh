#!/bin/bash

cat $1 \
    | ~/GOD.util/moses-scripts/scripts/generic/multi-bleu.perl -lc zh-en/valid.News.zh-en.zh \
    | sed -r 's/BLEU = ([0-9.]+),.*/\1/'

