#!/bin/bash -v

MARIAN=~/competence/build

MARIAN_TRAIN=$MARIAN/marian
MARIAN_DECODER=$MARIAN/marian-decoder
MARIAN_VOCAB=$MARIAN/marian-vocab
MARIAN_SCORER=$MARIAN/marian-scorer

# set chosen gpus
GPUS="0 1 2 3 4 5 6 7"
if [ $# -ne 0 ]
then
    GPUS=$@
fi
echo Using GPUs: $GPUS

SRCL=en
TGTL=zh
TERM=News
MODEL_NAME=BASE_BT_QKV
ID=2
MODEL_DIR=$MODEL_NAME\_$SRCL\-$TGTL
TRAIN=train.$TERM.$SRCL\-$TGTL
VALID=valid.$TERM.$SRCL\-$TGTL
CORPUS_DIR=/home/revo/golbin/patent/en-zh
OUTPUT_DIR=output

mkdir -p $MODEL_DIR
mkdir -p $OUTPUT_DIR

# create shared vocabulary
# if [ ! -e $MODEL_DIR"/vocab."$SRCL$TGTL".yml" ]
# then
#     cat $CORPUS_DIR/$TRAIN.$SRCL $CORPUS_DIR/$TRAIN.$TGTL | $MARIAN_VOCAB --max-size 66000 > $MODEL_DIR/vocab.$SRCL$TGTL.yml
# fi

# train model
    $MARIAN_TRAIN \
        --model $MODEL_DIR/model_revo.npz --type transformer \
        --train-sets $CORPUS_DIR/$TRAIN.$SRCL $CORPUS_DIR/$TRAIN.$TGTL \
        --max-length 200 \
        --vocabs $MODEL_DIR/vocab.$SRCL.yml $MODEL_DIR/vocab.$TGTL.yml \
        --mini-batch-fit -w 8500 --maxi-batch 1000 \
        --early-stopping 10 --cost-type=ce-mean-words \
        --valid-freq 5000 --save-freq 5000 --disp-freq 1 \
        --valid-metrics ce-mean-words perplexity translation \
        --valid-sets $CORPUS_DIR/$VALID.$SRCL $CORPUS_DIR/$VALID.$TGTL \
        --valid-script-path "bash ./validate-"$SRCL\-$TGTL".sh" \
        --valid-translation-output $OUTPUT_DIR/$MODEL_NAME.tf.$SRCL$TGTL.single --quiet-translation \
        --valid-mini-batch 30 \
        --beam-size 6 --normalize 0.6 \
        --log $MODEL_DIR/train.log --valid-log $MODEL_DIR/valid.log \
        --enc-depth 6 --dec-depth 6 \
        --transformer-heads 16 \
        --transformer-postprocess-emb d \
        --transformer-postprocess dan \
        --transformer-dropout 0.3 --label-smoothing 0.1 \
        --learn-rate 0.0007 --lr-warmup 16000 --lr-decay-inv-sqrt 16000 --lr-report \
        --optimizer-params 0.9 0.98 1e-09 --clip-norm 5 \
        --devices $GPUS --sync-sgd --seed $ID$ID$ID$ID --keep-best --overwrite \
        --exponential-smoothing \
        --dim-emb 512 --dim-trans 1024 --transformer-dim-ffn 4096 \
        --update_cycle 2
        # --sr-freq-file cl/$SRCL\-freq.txt cl/$SRCL\-cdf_base.npz 40000 0.01
