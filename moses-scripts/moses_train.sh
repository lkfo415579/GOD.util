corpus=train
f=zh
e=en
rootdir=moses-zh-en
lm=/home/mb45450/junk
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
-max-phrase-length 5
