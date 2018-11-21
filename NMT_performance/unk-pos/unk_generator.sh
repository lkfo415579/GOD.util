#!/bin/bash

# model
TERM=Common
SRCL=en
TGTL=zh
prefix=$TERM\_model-$SRCL\-$TGTL/model_revo_amun.npz

# decode

cat $1 | ~/marian_globon/build/amun -c $prefix.dev.npz.amun.yml -b 12 -n \
-u --return-alignment --mini-batch 10 --maxi-batch 100 -- \
    | ~/GOD.util/moses-scripts/scripts/recaser/detruecase.perl > $1.output

