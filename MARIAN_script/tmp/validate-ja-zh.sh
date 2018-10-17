#!/bin/bash

# model
TERM=Common
SRCL=ja
TGTL=zh
prefix=$TERM\_model-$SRCL\-$TGTL/model_revo_amun.npz
dev=$SRCL\-$TGTL/valid.$TERM.$SRCL\-$TGTL.$SRCL
ref=$SRCL\-$TGTL/valid.$TERM.$SRCL\-$TGTL.$TGTL

# decode

cat $dev | ~/marian_globon/build/amun -c $prefix.dev.npz.amun.yml -b 12 -n --mini-batch 10 --maxi-batch 100 2>/dev/null \
    | ~/GOD.util/moses-scripts/scripts/recaser/detruecase.perl > $dev.output.postprocessed

# get BLEU
~/GOD.util/moses-scripts/scripts/generic/multi-bleu.perl $ref < $dev.output.postprocessed | cut -f 3 -d ' ' | cut -f 1 -d ','
