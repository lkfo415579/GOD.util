SRCL=en
TGTL=zh
TERM=Medicine
CORPUS=/root/goblin/medicine
CORPUS=$(echo $CORPUS| sed 's/\//\\\//g')
rm -r tmp
mkdir -p tmp
cp train.big.enzh.sh tmp/train_$SRCL-$TGTL.sh
cp train.big.enzh.sh tmp/train_$TGTL-$SRCL.sh
cp validate.enzh.sh tmp/validate-$SRCL-$TGTL.sh
cp validate.enzh.sh tmp/validate-$TGTL-$SRCL.sh

# modify content
#SRCL->TGTL
TMP=s/SRCL=en/SRCL=${SRCL}/g
sed -i $TMP tmp/train_$SRCL-$TGTL.sh
sed -i $TMP tmp/validate-$SRCL-$TGTL.sh
TMP=s/TGTL=zh/TGTL=$TGTL/g
sed -i $TMP tmp/train_$SRCL-$TGTL.sh
sed -i $TMP tmp/validate-$SRCL-$TGTL.sh
#TGTL->SRCL
TMP=s/SRCL=en/SRCL=${TGTL}/g
sed -i $TMP tmp/train_$TGTL-$SRCL.sh
sed -i $TMP tmp/validate-$TGTL-$SRCL.sh
TMP=s/TGTL=zh/TGTL=$SRCL/g
sed -i $TMP tmp/train_$TGTL-$SRCL.sh
sed -i $TMP tmp/validate-$TGTL-$SRCL.sh
# term
TMP=s/TERM=News/TERM=$TERM/g
sed -i $TMP tmp/train_$SRCL-$TGTL.sh
sed -i $TMP tmp/validate-$SRCL-$TGTL.sh
sed -i $TMP tmp/train_$TGTL-$SRCL.sh
sed -i $TMP tmp/validate-$TGTL-$SRCL.sh
TMP='s/CORPUS_DIR=.*$/CORPUS_DIR='$CORPUS'\/'$SRCL-$TGTL'/g'
sed -i $TMP tmp/train_$SRCL-$TGTL.sh
TMP='s/CORPUS_DIR=.*$/CORPUS_DIR='$CORPUS'\/'$TGTL-$SRCL'/g'
sed -i $TMP tmp/train_$TGTL-$SRCL.sh
