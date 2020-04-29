#!/bin/bash -v

# MARIAN=~/competence/build
MARIAN=~/new_marian/build

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
MODEL_NAME=BASE
ID=2
MODEL_DIR=$MODEL_NAME\_$SRCL\-$TGTL
TRAIN=train.$TERM.$SRCL\-$TGTL
VALID=valid.$TERM.$SRCL\-$TGTL
CORPUS_DIR=$SRCL\-$TGTL
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
        --model $MODEL_DIR/model_revo.npz \
        --train-sets $CORPUS_DIR/$TRAIN.$SRCL $CORPUS_DIR/$TRAIN.$TGTL \
        --max-length 140 \
        --vocabs $MODEL_DIR/vocab.$SRCL.yml $MODEL_DIR/vocab.$TGTL.yml \
        --maxi-batch 20000 --mini-batch 64  -w 9000 --max-length-crop \
        --early-stopping 10 --cost-type=ce-sum \
        --valid-freq 2500 --save-freq 2500 --disp-freq 1 \
        --valid-metrics ce-mean-words perplexity translation \
        --valid-sets $CORPUS_DIR/$VALID.$SRCL $CORPUS_DIR/$VALID.$TGTL \
        --valid-script-path "bash ./validate-"$SRCL\-$TGTL".sh" \
        --valid-translation-output $OUTPUT_DIR/$MODEL_NAME.tf.$SRCL$TGTL.single --quiet-translation \
        --valid-mini-batch 30 \
        --beam-size 6 --normalize 1.0 \
        --log $MODEL_DIR/train.log --valid-log $MODEL_DIR/valid.log \
        --task transformer-base \
        --devices $GPUS --seed $ID$ID$ID$ID --keep-best --overwrite \
        --transformer-depth-scaling --enc-depth 20 --dec-depth 6 \
        --disp-label-counts --tied-embeddings-all false
