THUNMT=~/baseline/THUMT
SRCL=en
TGTL=zh
CORPUS_DIR=en-zh
CORPUS=$CORPUS_DIR/train.News.en-zh
GPUS=0
VALID=test/news.bpe
MODEL_DIR=train

if [ $# -ne 0 ]
then
    GPUS=$@
fi

 python $THUNMT/thumt/bin/translator.py \
     --input $VALID.$SRCL \
     --vocabulary $CORPUS_DIR/vocab.$SRCL.txt $CORPUS_DIR/vocab.$TGTL.txt \
     --models transformer transformer transformer transformer \
     --output test/output \
     --checkpoints $MODEL_DIR/eval/r1 $MODEL_DIR/eval/r2 $MODEL_DIR/eval/r3 $MODEL_DIR/eval/r4 \
     --parameters=device_list=[$GPUS],decode_alpha=0.6,beam_size=6


