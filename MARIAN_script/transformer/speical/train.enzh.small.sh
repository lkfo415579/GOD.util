#!/bin/bash -v

MARIAN=~/marian-dev/build

MARIAN_TRAIN=$MARIAN/marian
MARIAN_DECODER=$MARIAN/marian-decoder
MARIAN_VOCAB=$MARIAN/marian-vocab
MARIAN_SCORER=$MARIAN/marian-scorer

# set chosen gpus
GPUS=0
if [ $# -ne 0 ]
then
    GPUS=$@
fi
echo Using GPUs: $GPUS

SRCL=en
TGTL=zh
TERM=News
ID=2
MODEL_DIR=$ID\_TRANS_REVO_model_$SRCL\-$TGTL
TRAIN=train.$TERM.$SRCL\-$TGTL
VALID=valid.$TERM.$SRCL\-$TGTL
CORPUS_DIR=$SRCL-$TGTL
OUTPUT_DIR=output

mkdir -p $MODEL_DIR
mkdir -p $OUTPUT_DIR

# create common vocabulary
if [ ! -e $MODEL_DIR"/vocab."$SRCL".yml" ]
then
    cat $CORPUS_DIR/$TRAIN.$SRCL | $MARIAN_VOCAB --max-size 40000 > $MODEL_DIR/vocab.$SRCL.yml
    cat $CORPUS_DIR/$TRAIN.$TGTL | $MARIAN_VOCAB --max-size 40000 > $MODEL_DIR/vocab.$TGTL.yml
fi

# train model
    $MARIAN_TRAIN \
        --model $MODEL_DIR/model_revo.npz --type transformer \
        --train-sets $CORPUS_DIR/$TRAIN.$SRCL $CORPUS_DIR/$TRAIN.$TGTL \
        --max-length 140 \
        --vocabs $MODEL_DIR/vocab.$SRCL.yml $MODEL_DIR/vocab.$TGTL.yml \
        --mini-batch-fit -w 9500 --maxi-batch 1000 \
        --early-stopping 10 --cost-type=ce-mean-words \
        --valid-freq 5000 --save-freq 5000 --disp-freq 500 \
        --valid-metrics ce-mean-words perplexity translation \
        --valid-sets $CORPUS_DIR/$VALID.$SRCL $CORPUS_DIR/$VALID.$TGTL \
        --valid-script-path "bash ./validate-"$SRCL\-$TGTL".sh" \
        --valid-translation-output $OUTPUT_DIR/$ID.tf.$SRCL$TGTL.single --quiet-translation \
        --valid-mini-batch 64 \
        --beam-size 6 --normalize 0.6 \
        --log $MODEL_DIR/train.log --valid-log $MODEL_DIR/valid.log \
        --enc-depth 2 --dec-depth 2 \
        --transformer-heads 4 \
        --transformer-postprocess-emb d \
        --transformer-postprocess dan \
        --transformer-dropout 0.1 --label-smoothing 0.1 \
        --learn-rate 0.0003 --lr-warmup 16000 --lr-decay-inv-sqrt 16000 --lr-report \
        --optimizer-params 0.9 0.98 1e-09 --clip-norm 5 \
        --devices $GPUS --sync-sgd --seed $ID$ID$ID$ID --keep-best --overwrite \
        --exponential-smoothing --dim-emb 256 --transformer-decoder-autoreg average-attention
