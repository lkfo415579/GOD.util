THUNMT=~/baseline/THUMT
SRCL=en
TGTL=zh
CORPUS_DIR=en-zh
CORPUS=$CORPUS_DIR/train.News.en-zh
GPUS=1,2
VALID=test/news.bpe
MODEL_DIR=big_model

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

 python $THUNMT/thumt/bin/trainer.py \
    --input $CORPUS.$SRCL $CORPUS.$TGTL \
    --output $MODEL_DIR \
    --vocabulary $CORPUS_DIR/vocab.$SRCL.txt $CORPUS_DIR/vocab.$TGTL.txt \
    --model transformer\
    --validation $VALID.$SRCL \
    --references $VALID.$TGTL \
    --parameters=batch_size=6250,device_list=[$GPUS],train_steps=300000,update_cycle=2,hidden_size=512,filter_size=2048,num_heads=8

 python $THUNMT/thumt/bin/translator.py \
     --input $VALID.$SRCL \
     --vocabulary $CORPUS_DIR/vocab.$SRCL.txt $CORPUS_DIR/vocab.$TGTL.txt \
     --model transformer \
     --output test/output \
     --checkpoints $MODEL_DIR/eval \
     --parameters=device_list=[$GPUS],decode_alpha=0.6,beam_size=6


