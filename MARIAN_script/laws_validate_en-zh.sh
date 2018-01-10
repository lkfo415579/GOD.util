#!/bin/bash

# model prefix
prefix=Laws_model-en-zh/model_revo_amun.npz

dev=en-zh/valid.Laws.en-zh.en
ref=en-zh/valid.Laws.en-zh.zh

# decode

cat $dev | amun -c $prefix.dev.npz.amun.yml -b 12 -n --mini-batch 10 --maxi-batch 100 2>/dev/null \
    | $HOME/GOD.util/moses-scripts/scripts/recaser/detruecase.perl > $dev.output.postprocessed

# get BLEU
$HOME/GOD.util/moses-scripts/scripts/generic/multi-bleu.perl $ref < $dev.output.postprocessed | cut -f 3 -d ' ' | cut -f 1 -d ','
