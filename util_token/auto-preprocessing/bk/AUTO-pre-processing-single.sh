#!/bin/bash
#version1.0 revo,1/22/2018, AUTO-preprocessing en-zh,zh-en, and others
if [ "$1" == "-h"  ]; then
  echo 'Please modify your correct parameters.'
  echo 'Usage : ./AUTO-pre-processing.sh'
    exit 0
fi
SRCL=$1
TGTL=$2
CORPUS=$3
UTIL_FOLDER=.
# GOD_FOLDER=~/GOD.util
SUPER="python /home/training/GOD.util/super_tokenizer/super_tokenizer.py"
# SUPER=~/GOD.util/super_tokenizer/dist/super_tokenizer/super_tokenizer
echo "language order : ${1}->${2}"
if [ "$1" == "en"  ]; then
  $SUPER en -l < $CORPUS.$SRCL > $CORPUS.tok.$SRCL
  if [ "$2" == "zh"  ]; then
    $SUPER zh < $CORPUS.$TGTL > $CORPUS.tok.$TGTL
    $UTIL_FOLDER/escape-special-chars.perl < $CORPUS.tok.$TGTL > $CORPUS.esc.$TGTL
    mv $CORPUS.esc.$TGTL $CORPUS.tok.$TGTL
  fi
fi

if [ "$1" == "zh"  ]; then
  $SUPER zh < $CORPUS.$SRCL > $CORPUS.tok.$SRCL
  $UTIL_FOLDER/replace-unicode-punctuation.perl < $CORPUS.tok.$SRCL > $CORPUS.replace.$SRCL
  $UTIL_FOLDER/escape-special-chars.perl < $CORPUS.replace.$SRCL > $CORPUS.esc.$SRCL
  mv $CORPUS.esc.$SRCL $CORPUS.tok.$SRCL
  rm $CORPUS.replace.$SRCL
  if [ "$2" == "en"  ]; then
    $SUPER en < $CORPUS.$TGTL > $CORPUS.tok.$TGTL
  fi
fi

echo "Cleaning created files"
$UTIL_FOLDER/clean-corpus-n.perl $CORPUS.tok $SRCL $TGTL $CORPUS.${SRCL}-${TGTL}.clean 1 150
rm $CORPUS.tok.$SRCL $CORPUS.tok.$TGTL
