TERM=News
CORPUS_PATH=..
mkdir -p $TERM
python ~/GOD.util/BPE_TOOLKIT/apply_bpe_unk2.py -c $CORPUS_PATH/$TERM/en-zh/en.bpe < 34k.unk2.en-zh.en > $TERM/unk2.en-zh.b.en
python ~/GOD.util/BPE_TOOLKIT/apply_bpe_unk2.py -c $CORPUS_PATH/$TERM/en-zh/zh.bpe < 34k.unk2.en-zh.zh > $TERM/unk2.en-zh.b.zh
python ~/GOD.util/BPE_TOOLKIT/apply_bpe_unk2.py -c $CORPUS_PATH/$TERM/zh-en/en.bpe < 34k.unk2.zh-en.en > $TERM/unk2.zh-en.b.en
python ~/GOD.util/BPE_TOOLKIT/apply_bpe_unk2.py -c $CORPUS_PATH/$TERM/zh-en/zh.bpe < 34k.unk2.zh-en.zh > $TERM/unk2.zh-en.b.zh

echo "EN-zh"
cat $TERM/unk2.en-zh.b.en >> $CORPUS_PATH/$TERM/en-zh/train.$TERM.en-zh.en
cat $TERM/unk2.en-zh.b.zh >> $CORPUS_PATH/$TERM/en-zh/train.$TERM.en-zh.zh
head -n 200 $TERM/unk2.en-zh.b.en >> $CORPUS_PATH/$TERM/en-zh/valid.$TERM.en-zh.en
head -n 200 $TERM/unk2.en-zh.b.zh >> $CORPUS_PATH/$TERM/en-zh/valid.$TERM.en-zh.zh

echo "zh-EN"
cat $TERM/unk2.zh-en.b.en >> $CORPUS_PATH/$TERM/zh-en/train.$TERM.zh-en.en
cat $TERM/unk2.zh-en.b.zh >> $CORPUS_PATH/$TERM/zh-en/train.$TERM.zh-en.zh
head -n 200 $TERM/unk2.zh-en.b.en >> $CORPUS_PATH/$TERM/zh-en/valid.$TERM.zh-en.en
head -n 200 $TERM/unk2.zh-en.b.zh >> $CORPUS_PATH/$TERM/zh-en/valid.$TERM.zh-en.zh
