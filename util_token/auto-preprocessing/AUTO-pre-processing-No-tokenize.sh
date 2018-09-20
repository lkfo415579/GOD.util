#!/bin/bash
#version2.0 revo,1/22/2018, AUTO-preprocessing en-zh,zh-en, and others
if [ "$1" == "-h"  ]; then
  echo 'Please modify your correct parameters.'
  echo 'Usage : ./AUTO-pre-processing.sh CORPUS'
    exit 0
fi

CORPUS=$1
UTIL_FOLDER=~/GOD.util/util_token
# GOD_FOLDER=~/GOD.util
SUPER="python /home/training/GOD.util/super_tokenizer/super_tokenizer.py"
# SUPER=~/GOD.util/super_tokenizer/dist/super_tokenizer/super_tokenizer
echo "No eng tokenizer, language order : en->zh && zh->en"
cp $CORPUS.en $CORPUS.tok.en
cp $CORPUS.en $CORPUS.en-zh.tok.en
# $SUPER en < $CORPUS.en > $CORPUS.tok.en
$SUPER zh < $CORPUS.zh > $CORPUS.tok.zh
# en->zh
$UTIL_FOLDER/escape-special-chars.perl < $CORPUS.tok.zh > $CORPUS.en-zh.esc.zh
mv $CORPUS.en-zh.esc.zh $CORPUS.en-zh.tok.zh
# zh->en
$UTIL_FOLDER/replace-unicode-punctuation.perl < $CORPUS.tok.zh > $CORPUS.replace.zh
$UTIL_FOLDER/escape-special-chars.perl < $CORPUS.replace.zh > $CORPUS.zh-en.esc.zh
cp $CORPUS.tok.en $CORPUS.zh-en.tok.en
mv $CORPUS.zh-en.esc.zh $CORPUS.zh-en.tok.zh

rm $CORPUS.tok.en
rm $CORPUS.tok.zh
rm $CORPUS.replace.zh

echo "Cleaning created files en-zh"
$UTIL_FOLDER/clean-corpus-n.perl $CORPUS.en-zh.tok en zh $CORPUS.en-zh.clean 1 150
rm $CORPUS.en-zh.tok.*

echo "Cleaning created files zh-en"
$UTIL_FOLDER/clean-corpus-n.perl $CORPUS.zh-en.tok en zh $CORPUS.zh-en.clean 1 150
rm $CORPUS.zh-en.tok.*
