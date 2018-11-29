SCRIPT=~/GOD.util/BPE_TOOLKIT/apply_bpe_unk2.py
SRCL=en
TGTL=de
# ST=${SRCL}-${TGTL}
# import
TERM=Common
CORPUS_DIR=..
python $SCRIPT -c $CORPUS_DIR/$SRCL-$TGTL/$SRCL.bpe < unk.$SRCL-$TGTL.$SRCL > tmp.$SRCL
python $SCRIPT -c $CORPUS_DIR/$SRCL-$TGTL/$TGTL.bpe < unk.$SRCL-$TGTL.$TGTL > tmp.$TGTL
#
python $SCRIPT -c $CORPUS_DIR/$TGTL-$SRCL/$SRCL.bpe < unk.$TGTL-$SRCL.$SRCL > tmp.2.$SRCL
python $SCRIPT -c $CORPUS_DIR/$TGTL-$SRCL/$TGTL.bpe < unk.$TGTL-$SRCL.$TGTL > tmp.2.$TGTL

cat tmp.$SRCL >> $CORPUS_DIR/$SRCL-$TGTL/train.$TERM.$SRCL-$TGTL.$SRCL
cat tmp.$TGTL >> $CORPUS_DIR/$SRCL-$TGTL/train.$TERM.$SRCL-$TGTL.$TGTL
cat tmp.2.$SRCL >> $CORPUS_DIR/$TGTL-$SRCL/train.$TERM.$TGTL-$SRCL.$SRCL
cat tmp.2.$TGTL >> $CORPUS_DIR/$TGTL-$SRCL/train.$TERM.$TGTL-$SRCL.$TGTL

rm tmp*
