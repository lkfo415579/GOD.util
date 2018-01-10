#!/bin/bash

# set chosen gpus
GPUS="0 1 2 3"
SRCL=en
TGTL=zh
CORPUS=train.Laws.en-zh
CORPUS_DIR=/home/revo/workshop/laws/en-zh
MODELS_DIR=Laws_model-en-zh
DEV_SET=valid.Laws.en-zh
if [ $# -ne 0 ]
then
    GPUS=$@
fi
echo Using gpus $GPUS


if [ ! -e $MODELS_DIR ]
then
    mkdir -p $MODELS_DIR
fi

# train model

    marian \
        --model $MODELS_DIR/model_revo_amun.npz \
        --type amun \
        --devices $GPUS --seed 0 \
        --train-sets $CORPUS_DIR/$CORPUS.$SRCL $CORPUS_DIR/$CORPUS.$TGTL \
        --max-length 120 \
        --vocabs $MODELS_DIR/vocab.$SRCL.yml $MODELS_DIR/vocab.$TGTL.yml \
        --dim-vocabs 70000 66666 \
        --dynamic-batching -w 3000 \
        --layer-normalization --dropout-rnn 0.2 --dropout-src 0.1 --dropout-trg 0.1 \
        --early-stopping 5 --moving-average \
        --dim-emb 630 \
        --valid-freq 25000 --save-freq 50000 --disp-freq 1000 \
        --valid-sets $CORPUS_DIR/$DEV_SET.$SRCL $CORPUS_DIR/$DEV_SET.$TGTL \
        --valid-metrics cross-entropy valid-script \
        --valid-script-path ./laws_validate_en-zh.sh \
        --log $MODELS_DIR/train.log --valid-log $MODELS_DIR/valid.log


