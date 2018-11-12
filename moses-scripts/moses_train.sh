corpus=train.clean
f=en
e=zh
rootdir=moses-zh-en
lm=/home/training/LEXICON_WORKSHOP
firststep=4
laststep=4
~/mosesdecoder/scripts/training/train-model.perl \
-root-dir $rootdir \
-corpus $corpus \
-f $f -e $e \
-alignment grow-diag-final-and \
-reordering distance,msd-bidirectional-fe \
-lm 0:5:$lm:9 \
-first-step $firststep -last-step $laststep \
-external-bin-dir ~/mosesdecoder/tools \
-max-phrase-length 5
