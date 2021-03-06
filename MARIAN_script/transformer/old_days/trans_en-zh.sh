#!/bin/bash -v

MARIAN=~/marian-dev
GPUS="0 1 2 3"
SRCL=en
TGTL=zh
TERM=News
CORPUS=train.$TERM.$SRCL-$TGTL
CORPUS_DIR=/data/marian-examples/goblin/goddess/en-zh
MODELS_DIR=$TERM_MODEL_COM_$SRCL-$TGTL
DEV_SET=valid.$TERM.$SRCL-$TGTL
# set chosen gpus
if [ $# -ne 0 ]
then
    GPUS=$@
fi
echo Using GPUs: $GPUS

if [ ! -e $MARIAN/build/marian ]
then
    echo "marian is not installed in ../../build, you need to compile the toolkit first"
    exit 1
fi


mkdir -p $MODELS_DIR

# preprocess data

# create common vocabulary
if [ ! -e "$MODELS_DIR/vocab.$SRCL$TGTL.yml" ]
then
    cat $CORPUS_DIR/$CORPUS.$SRCL | $MARIAN/build/marian-vocab --max-size 50000 > $MODELS_DIR/vocab.$SRCL.yml
    cat $CORPUS_DIR/$CORPUS.$TGTL | $MARIAN/build/marian-vocab --max-size 50000 > $MODELS_DIR/vocab.$TGTL.yml
fi
#exit
# train $MODELS_DIR
    $MARIAN/build/marian \
        --model $MODELS_DIR/model_revo_trans.npz --type transformer \
        --train-sets $CORPUS_DIR/$CORPUS.$SRCL $CORPUS_DIR/$CORPUS.$TGTL \
        --max-length 140 \
        --vocabs $MODELS_DIR/vocab.$SRCL.yml $MODELS_DIR/vocab.$TGTL.yml \
        --mini-batch-fit -w 7000 --maxi-batch 1000 \
        --early-stopping 10 --cost-type=ce-mean-words \
        --valid-freq 5000 --save-freq 5000 --disp-freq 500 \
        --valid-metrics ce-mean-words perplexity translation \
        --valid-sets $CORPUS_DIR/$DEV_SET.$SRCL $CORPUS_DIR/$DEV_SET.$TGTL \
        --valid-script-path ./validate_$SRCL-$TGTL.sh \
        --valid-translation-output $CORPUS_DIR/$DEV_SET.2.output --quiet-translation \
        --valid-mini-batch 64 \
        --beam-size 6 --normalize 0.6 \
        --log $MODELS_DIR/train.log --valid-log $MODELS_DIR/valid.log \
        --enc-depth 6 --dec-depth 6 \
        --transformer-heads 8 \
        --transformer-postprocess-emb d \
        --transformer-postprocess dan \
        --transformer-dropout 0.1 --label-smoothing 0.1 \
        --learn-rate 0.0003 --lr-warmup 16000 --lr-decay-inv-sqrt 16000 --lr-report \
        --optimizer-params 0.9 0.98 1e-09 --clip-norm 5 \
        --devices $GPUS --sync-sgd --seed 1111

