#!/bin/bash
if [ $# -ne 5 ]; then
   echo "Usage: $0 corpus srcl tgtl validate size"
   exit;
fi

DELIMTER='@@@@@@@@@@'
BASEDIR=`realpath $0`                                                                                                    
BASEDIR=${BASEDIR%/*}

CORPUS=$1
SRCL=$2
TGTL=$3
VALIDATE=$4
SIZE=$5
#TOTALSIZE=$[$SIZE*2]

#echo $SIZE
#echo $TOTALSIZE
#exit

TMP_OUTPUT=.tmp.corpus.shuf
python $BASEDIR/merge.py -s $CORPUS.$SRCL -t $CORPUS.$TGTL |shuf >$TMP_OUTPUT
#paste -d $${DELIMTER} $CORPUS.$SRCL $CORPUS.$TGTL | shuf > $TMP_OUTPUT

TMP_INPUT=$TMP_OUTPUT
TMP_OUTPUT=.tmp.valid.shuf
head -n $SIZE   $TMP_INPUT > $TMP_OUTPUT

sed -i "s/${DELIMTER}/\n/g" $TMP_OUTPUT
TMP_INPUT=$TMP_OUTPUT
TMP_OUTPUT=$VALIDATE.$SRCL
awk 'NR%2' $TMP_INPUT > $TMP_OUTPUT

TMP_OUTPUT=$VALIDATE.$TGTL
awk '!(NR%2)' $TMP_INPUT > $TMP_OUTPUT

TMP_INPUT=.tmp.corpus.shuf
TMP_OUTPUT=.tmp.corpus.shuf.remove
sed "1, ${SIZE}d" $TMP_INPUT > $TMP_OUTPUT
sed -i "s/${DELIMTER}/\n/g" $TMP_OUTPUT

TMP_INPUT=$TMP_OUTPUT
awk 'NR%2' $TMP_INPUT > $CORPUS.remove-head.$SRCL
awk '!(NR%2)' $TMP_INPUT > $CORPUS.remove-head.$TGTL

rm -rf  .tmp.corpus.shuf 
rm -rf  .tmp.corpus.shuf.remove 
rm -rf  .tmp.valid.shuf 
