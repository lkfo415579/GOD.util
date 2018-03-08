#!/bin/bash
#version1.2 revo,12/22/2017, including filtering and duplicated corpus remove
if [ "$1" == "-h"  ]; then
  echo 'Please modify your correct path.'
  echo 'Usage : ./pre'
    exit 0
fi
echo "DUPLICATE_FILTER_PRE script starting, version:2.0"
# source language (example: fr)
SRCL=en
# target language (example: en)
TGTL=zh
# corpus
P=Bi-additional-en-zh-clean
# script folder
P1=~/GOD.util/BPE_TOOLKIT
# BPE setting
NUM=30000
CORPUS=${P}.bpe
TERM=ADD
OPERATION=70000
# Duplicated remove python
DUPLICATE=1
FILTER=0
#
SRCL_FILE=$P.$SRCL
TGTL_FILE=$P.$TGTL
if [ "$DUPLICATE" == "1"  ]; then
  echo "Duplication cleaning"
  python $P1/cleanDuplicateOrderParallax.py $P.$SRCL $P.$TGTL
  # auto output to .uni
  # pair lang cheking
  mv $P.$SRCL.uni $P.uni.$SRCL
  mv $P.$TGTL.uni $P.uni.$TGTL

  if [ "$FILTER" == "1"  ]; then
    python $P1/pair_lang_filter.py $P.uni $TGTL $SRCL $P.filter
    # cleaning
    rm $P.uni.$SRCL $P.uni.$TGTL
  else
    mv $P.uni.$SRCL $P.filter.$SRCL
    mv $P.uni.$TGTL $P.filter.$TGTL
  fi
  SRCL_FILE=$P.filter.$SRCL
  TGTL_FILE=$P.filter.$TGTL
fi
#
# learn BPE on joint vocabulary
echo "Seprerate BPE VERSION"
# echo "EMAIL&URL APPLY BPE"
echo "Learning BPE"
cat $SRCL_FILE | python $P1/learn_bpe.py -s $OPERATION > ${SRCL}.bpe
cat $TGTL_FILE | python $P1/learn_bpe.py -s $OPERATION > ${TGTL}.bpe
echo "Applying BPE"
python $P1/apply_bpe.py -c ${SRCL}.bpe < $SRCL_FILE > ${P}.bpe.${SRCL}
python $P1/apply_bpe.py -c ${TGTL}.bpe < $TGTL_FILE > ${P}.bpe.${TGTL}
echo "Remove tmp file"
rm $P.filter.$SRCL $P.filter.$TGTL
# shuffle data
paste -d $'\t' $CORPUS.$SRCL $CORPUS.$TGTL | shuf > $CORPUS.shuf
head -n $NUM $CORPUS.shuf | cut -d $'\t' -f1 > valid.$TERM.$SRCL-$TGTL.$SRCL
head -n $NUM $CORPUS.shuf | cut -d $'\t' -f2 > valid.$TERM.$SRCL-$TGTL.$TGTL
sed '1,'$NUM'd' $CORPUS.shuf | cut -d $'\t' -f1 > train.$TERM.$SRCL-$TGTL.$SRCL
sed '1,'$NUM'd' $CORPUS.shuf | cut -d $'\t' -f2 > train.$TERM.$SRCL-$TGTL.$TGTL
rm $CORPUS.shuf
