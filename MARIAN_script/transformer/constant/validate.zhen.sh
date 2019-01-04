#!/bin/bash

cat $1 \
    | sed 's/\@\@ //g' \
    | ~/GOD.util/util_token/detokenize.py -l en \
    | sed 's/  / /g' | sed 's/  / /g' \
    | python ~/GOD.util/util_token/tokenize.py \
    | ~/GOD.util/moses-scripts/scripts/generic/multi-bleu.perl -lc brave/news.zhen.tok.en \
    | sed -r 's/BLEU = ([0-9.]+),.*/\1/'
#  ~/moses-scripts/scripts/recaser/detruecase.perl 2> /dev/null \
#  ~/moses-scripts/scripts/tokenizer/detokenizer.perl -l en 2>/dev/null \
