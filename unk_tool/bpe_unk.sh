SCRIPT=~/GOD.util/BPE_TOOLKIT/apply_bpe_unk2.py
# SRCL=en
# TGTL=zh
# ST=${SRCL}-${TGTL}
# import
TERM=Engine
CORPUS_DIR=..
python $SCRIPT -c $CORPUS_DIR/en-zh/en.bpe < unk.en-zh.en > tmp.en
python $SCRIPT -c $CORPUS_DIR/en-zh/zh.bpe < unk.en-zh.zh > tmp.zh
#
python $SCRIPT -c $CORPUS_DIR/zh-en/en.bpe < unk.zh-en.en > tmp.2.en
python $SCRIPT -c $CORPUS_DIR/zh-en/zh.bpe < unk.zh-en.zh > tmp.2.zh

cat tmp.en >> $CORPUS_DIR/en-zh/train.$TERM.en-zh.en
cat tmp.zh >> $CORPUS_DIR/en-zh/train.$TERM.en-zh.zh
cat tmp.2.en >> $CORPUS_DIR/zh-en/train.$TERM.zh-en.en
cat tmp.2.zh >> $CORPUS_DIR/zh-en/train.$TERM.zh-en.zh

rm tmp*
