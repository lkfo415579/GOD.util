#!/bin/bash

# set chosen gpus
GPUS="4 5 6 7"
#GPUS="0 1 2 3"
SRCL=zh
TGTL=ja
TERM=Common
CORPUS=train.$TERM.$SRCL\-$TGTL
CORPUS_DIR=/data/ja-zh
MODELS_DIR=${TERM}_model-${SRCL}-${TGTL}
DEV_SET=valid.$TERM.$SRCL\-$TGTL
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

    ~/marian_globon/build/marian \
        --model $MODELS_DIR/model_revo_amun.npz \
        --type amun \
        --devices $GPUS --seed 2222 \
        --train-sets $CORPUS_DIR/$CORPUS.$SRCL $CORPUS_DIR/$CORPUS.$TGTL \
        --max-length 140 \
        --vocabs $MODELS_DIR/vocab.$SRCL.yml $MODELS_DIR/vocab.$TGTL.yml \
        --dim-vocabs 71111 66666 \
        --dynamic-batching -w 3000 \
        --layer-normalization --dropout-rnn 0.2 --dropout-src 0.1 --dropout-trg 0.1 \
        --early-stopping 5 --moving-average \
        --dim-emb 512 \
        --valid-freq 25000 --save-freq 50000 --disp-freq 1000 \
        --valid-sets $CORPUS_DIR/$DEV_SET.$SRCL $CORPUS_DIR/$DEV_SET.$TGTL \
        --valid-metrics cross-entropy valid-script \
        --valid-script-path ./validate-${SRCL}-${TGTL}.sh \
        --keep-best \
        --lr-decay 0.1 \
        --log $MODELS_DIR/train.log --valid-log $MODELS_DIR/valid.log


