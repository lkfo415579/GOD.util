THUNMT=~/THUMT
SRCL=en
TGTL=zh
CORPUS_DIR=en-zh
CORPUS=en-zh/train.News.en-zh
GPUS=1,2
if [ $# -ne 0 ]
then
    GPUS=$@
fi

if [ ! -e $CORPUS_DIR/vocab.$SRCL.txt ]
then
    echo "Generating Voc."
    python $THUNMT/thumt/scripts/build_vocab.py $CORPUS.$SRCL $CORPUS_DIR/vocab.$SRCL
    python $THUNMT/thumt/scripts/build_vocab.py $CORPUS.$TGTL $CORPUS_DIR/vocab.$TGTL
fi

 python $THUNMT/thumt/bin/trainer.py --input $CORPUS.$SRCL $CORPUS.$TGTL \
    --vocabulary $CORPUS_DIR/vocab.$SRCL.txt $CORPUS_DIR/vocab.$TGTL.txt \
    --model transformer --validation $CORPUS_DIR/valid.News.en-zh.en \
    --references $CORPUS_DIR/valid.News.en-zh.zh \
    --parameters=batch_size=6250,device_list=[$GPUS],train_steps=200000
