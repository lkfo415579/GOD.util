#!/bin/bash

# decode
prefix=GOBLIN_NEW_MODEL_COM/model_revo_trans.npz

cat $1 | ~/marian-dev/build/marian-decoder -c $prefix.decoder.yml -b 6 -n 0.6 \
--mini-batch 10 -d 4 5 6 --maxi-batch 100 \
--quiet-translation 2>/dev/null \
    | ~/GOD.util/moses-scripts/scripts/recaser/detruecase.perl > $1.output.postprocessed

# get BLEU
cat $1.output.postprocessed | sed 's/@@ //g' \
    | ~/GOD.util/moses-scripts/scripts/generic/multi-bleu.perl $2

