#!/bin/bash

SRCL=en
TGTL=zh
TERM=News
VALID=$SRCL\-$TGTL/valid.$TERM.$SRCL\-$TGTL.$TGTL

cat $1 | sed 's/@@ //g'\
    | ~/GOD.util/moses-scripts/scripts/generic/multi-bleu.perl -lc $VALID \
    | sed -r 's/BLEU = ([0-9.]+),.*/\1/'
