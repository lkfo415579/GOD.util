#!/bin/bash

if [ "$1" == "-h"   ]; then
  echo 'revo_version'
    echo 'Usage : ./preprocess.sh '
    exit 0
fi

# source language (example: fr)
S=en
# target language (example: en)
T=zh
# data
TERM=Computer
P=train.tok
# data folder
#PATH=$4
# script folder
P1=.


# learn BPE on joint vocabulary:
echo "Learning BPE"
cat ${P}.${S}  | python $P1/learn_bpe.py -s 120000 > ${S}.bpe
cat ${P}.${T}  | python $P1/learn_bpe.py -s 120000 > ${T}.bpe
echo "Applying BPE"
python $P1/apply_bpe.py -c ${S}.bpe < ${P}.${S} > ${P}.bpe.${S}
python $P1/apply_bpe.py -c ${T}.bpe < ${P}.${T} > ${P}.bpe.${T}

#NUM=40000
#CORPUS=${P}.bpe
#paste -d $'\t' $CORPUS.$S $CORPUS.$T | shuf > $CORPUS.shuf
#head -n $NUM $CORPUS.shuf | cut -d $'\t' -f1 > valid.$TERM.$S-$T.$S
#head -n $NUM $CORPUS.shuf | cut -d $'\t' -f2 > valid.$TERM.$S-$T.$T
#sed '1,'$NUM'd' $CORPUS.shuf | cut -d $'\t' -f1 > train.$TERM.$S-$T.$S
#sed '1,'$NUM'd' $CORPUS.shuf | cut -d $'\t' -f2 > train.$TERM.$S-$T.$T

