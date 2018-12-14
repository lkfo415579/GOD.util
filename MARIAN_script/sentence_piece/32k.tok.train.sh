#!/bin/bash -v

MARIAN=~/marians/marian-dev

# set chosen gpus
GPUS=0
if [ $# -ne 0 ]
then
    GPUS=$@
fi
echo Using GPUs: $GPUS

if [ ! -e $MARIAN/build/marian ]
then
    echo "marian is not installed in $MARIAN/build, you need to compile the toolkit first"
    exit 1
fi

# parameters
MODEL_DIR=32k_tok_model
SRCL=en
TGTL=zh
# DATA=en-zh/origin/all
DATA=en-zh/32k/train.News
VALID=test/news

# create the $MODEL_DIR folder
mkdir -p $MODEL_DIR

# train $MODEL_DIR
$MARIAN/build/marian \
    --devices $GPUS \
    --type amun \
    --model $MODEL_DIR/model_revo.npz \
    --train-sets $DATA.$SRCL $DATA.$TGTL \
    --vocabs $MODEL_DIR/vocab.$SRCL$TGTL.spm $MODEL_DIR/vocab.$SRCL$TGTL.spm \
    --dim-vocabs 32000 32000 \
    --mini-batch-fit -w 5000 \
    --layer-normalization --tied-embeddings-all \
    --dropout-rnn 0.2 --dropout-src 0.1 --dropout-trg 0.1 \
    --early-stopping 5 --max-length 100 \
    --valid-freq 10000 --save-freq 10000 --disp-freq 1000 \
    --cost-type ce-mean-words --valid-metrics ce-mean-words translation \
    --valid-sets $VALID.$SRCL test/news.tok.zh \
    --valid-script-path "bash ./validate.sh" \
    --valid-translation-output $VALID.$SRCL.output.2 \
    --log $MODEL_DIR/train.log --valid-log $MODEL_DIR/valid.log --tempdir $MODEL_DIR \
    --overwrite --keep-best \
    --seed 1111 --exponential-smoothing \
    --normalize=0.6 --beam-size=6 --quiet-translation
