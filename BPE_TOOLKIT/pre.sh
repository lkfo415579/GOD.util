#!/bin/bash
#version1.2 revo,12/22/2017, including filtering and duplicated corpus remove
if [ "$1" == "-h"  ]; then
  echo 'Please modify your correct path.'
  echo 'Usage : ./pre'
    exit 0
fi

# source language (example: fr)
SRCL=en
# target language (example: en)
TGTL=zh
# data
P=Bi-News-en-zh-filter
# script folder
P1=~/GOD.util/BPE_TOOLKIT

# learn BPE on joint vocabulary
echo "Seprerate BPE VERSION"
echo "EMAIL&URL APPLY BPE"
echo "Learning BPE"
cat ${P}.${SRCL} | python $P1/learn_bpe.py -s 70000 > ${SRCL}.bpe
cat ${P}.${TGTL} | python $P1/learn_bpe.py -s 70000 > ${TGTL}.bpe
echo "Applying BPE"
python $P1/apply_bpe.py -c ${SRCL}.bpe < ${P}.${SRCL} > ${P}.bpe.${SRCL}
python $P1/apply_bpe.py -c ${TGTL}.bpe < ${P}.${TGTL} > ${P}.bpe.${TGTL}

# SHUFFLE
NUM=30000
CORPUS=${P}.bpe
TERM=News
paste -d $'\t' $CORPUS.$SRCL $CORPUS.$TGTL | shuf > $CORPUS.shuf
head -n $NUM $CORPUS.shuf | cut -d $'\t' -f1 > valid.$TERM.$SRCL-$TGTL.$SRCL
head -n $NUM $CORPUS.shuf | cut -d $'\t' -f2 > valid.$TERM.$SRCL-$TGTL.$TGTL
sed '1,'$NUM'd' $CORPUS.shuf | cut -d $'\t' -f1 > train.$TERM.$SRCL-$TGTL.$SRCL
sed '1,'$NUM'd' $CORPUS.shuf | cut -d $'\t' -f2 > train.$TERM.$SRCL-$TGTL.$TGTL
# Remove tmp data
rm $CORPUS.shuf
rm ${P}.bpe.${SRCL}
rm ${P}.bpe.${TGTL}
