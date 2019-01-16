echo "TRANSFORMER_VERSION"
if [ "$1" == "-h" ]; then
  echo "Usage: `basename $0` [BPE_FILE]"
  exit 0
fi
P=~/GOD.util/average_tool
# choose first top3 models
TOP=3
BPE=$1
echo "BPE file : "$BPE
MODELS=""
MODELS=$(cat valid.log | grep translation | sort -rg -k8,8 -t ' ' | cut -f 8 -d ' ' | head -n 12 \
| awk '{if ($0 % 5000 == 0) {print "model_revo.iter"$0".npz"}}')

TMP=($MODELS)
MODELS=""
for (( i = 0; i < $TOP; i++ )); do
  MODELS="$MODELS ${TMP[$i]}"
done
# MODELS=($MODELS)
echo "TOP3 models are : "$MODELS

python $P/average.py -m $MODELS -o model_revo_amun.avg.npz

tar zcvf TMP_MODEL.tar.gz model_revo_amun.avg.npz vocab* valid* $BPE
