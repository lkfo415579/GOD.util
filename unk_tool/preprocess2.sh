#!/bin/bash

if [ $#  -ne 4 ];then
   echo "Usage: $0 corpus.path srcl tgtl dict_size"
   exit;
fi

BASEDIR=`realpath $0`
BASEDIR=${BASEDIR%/*}

#P=/home/liangss/training/models/News/en-zh/Bi-Training-News-Finance-en-zh-clean

# source language (example: fr)
#S=en
# target language (example: en)
#T=zh

# path to subword NMT scripts (can be downloaded from https://github.com/rsennrich/subword-nmt)
P=$1
S=$2
T=$3
SIZE=$4
P2=$BASEDIR/subword-nmt

# learn BPE on joint vocabulary:
#cat ${P}.${S} ${P}.${T} | python $P2/learn_bpe.py -s $SIZE > ${S}${T}.bpe
cat ${P}.${S} | python $P2/learn_bpe.py -s $SIZE > ${S}.bpe
cat ${P}.${T} | python $P2/learn_bpe.py -s $SIZE > ${T}.bpe

python $P2/apply_bpe.py --glossaries '<unk2>' -c ${S}.bpe < ${P}.${S} > ${P}.bpe.${S}
python $P2/apply_bpe.py --glossaries '<unk2>' -c ${T}.bpe < ${P}.${T} > ${P}.bpe.${T}
