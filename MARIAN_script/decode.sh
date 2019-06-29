#!/bin/bash -v

MARIAN=~/marian-dev/build
MARIAN_DECODER=$MARIAN/marian-decoder
MODEL=BASE-small_2_REVO_en-zh
GPU="0"
$MARIAN_DECODER -c $MODEL/model_revo.npz.best-perplexity.npz.decoder.yml -o output.txt -d $GPU -b 6 < $1
