#!/bin/bash -v

MARIAN=~/marian-dev/build

MARIAN_TRAIN=$MARIAN/marian$EXT
MARIAN_DECODER=$MARIAN/marian-decoder$EXT
MARIAN_VOCAB=$MARIAN/marian-vocab$EXT
MARIAN_SCORER=$MARIAN/marian-scorer$EXT

# set chosen gpus
GPUS=0
if [ $# -ne 0 ]
then
    GPUS=$@
fi
echo Using GPUs: $GPUS

SRCL=zh
TGTL=en
TERM=News
MODEL_DIR=SINGLE_TRANS_REVO_model_$SRCL\-$TGTL
DATA=$SRCL-$TGTL/train.$TERM.$SRCL\-$TGTL
VALID=brave/news.$SRCL$TGTL.bpe
OUTPUT_DIR=output
ID=2
mkdir -p $MODEL_DIR
mkdir -p $OUTPUT_DIR

# create common vocabulary
# if [ ! -e $MODEL_DIR"/vocab."$SRCL$TGTL".yml" ]
# then
#     cat $DATA.$SRCL $DATA.$TGTL | $MARIAN_VOCAB --max-size 66000 > $MODEL_DIR/vocab.$SRCL$TGTL.yml
# fi

# train model
    $MARIAN_TRAIN \
        --model $MODEL_DIR/model_revo.npz --type transformer \
        --train-sets $DATA.$SRCL $DATA.$TGTL \
        --max-length 100 \
        --vocabs $MODEL_DIR/vocab.$SRCL.yml $MODEL_DIR/vocab.$TGTL.yml \
        --mini-batch-fit -w 9500 --maxi-batch 1000 \
        --early-stopping 10 --cost-type=ce-mean-words \
        --valid-freq 5000 --save-freq 5000 --disp-freq 500 \
        --valid-metrics ce-mean-words perplexity translation \
        --valid-sets $VALID.$SRCL $VALID.$TGTL \
        --valid-script-path "bash ./validate."$SRCL$TGTL".sh" \
        --valid-translation-output $OUTPUT_DIR/tf.$SRCL$TGTL.single --quiet-translation \
        --valid-mini-batch 64 \
        --beam-size 6 --normalize 0.6 \
        --log $MODEL_DIR/train.log --valid-log $MODEL_DIR/valid.log \
        --enc-depth 6 --dec-depth 6 \
        --transformer-heads 8 \
        --transformer-postprocess-emb d \
        --transformer-postprocess dan \
        --transformer-dropout 0.1 --label-smoothing 0.1 \
        --learn-rate 0.0003 --lr-warmup 16000 --lr-decay-inv-sqrt 16000 --lr-report \
        --optimizer-params 0.9 0.98 1e-09 --clip-norm 5 \
        --devices $GPUS --sync-sgd --seed $ID$ID$ID$ID --keep-best \
        --exponential-smoothing
