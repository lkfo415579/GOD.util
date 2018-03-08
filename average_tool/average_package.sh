if [ "$1" == "-h" ]; then
  echo "Usage: `basename $0` [BPE_FILE]"
  exit 0
fi
P=~/GOD.util/average_tool
# choose first top3 models
TOP=3
BPE=$1
echo "BPE file : "$BPE
# cat valid.log | grep valid-script | sort -rg -k8,8 -t ' ' | cut -f 4 -d ' ' | head -n 12 | xargs -I {} echo model_revo_amun.iter{}.npz
MODELS=""
MODELS=$(cat valid.log | grep valid-script | sort -rg -k8,8 -t ' ' | cut -f 4 -d ' ' | head -n 12 \
| awk '{if ($0 % 50000 == 0) {print "model_revo_amun.iter"$0".npz"}}')

TMP=($MODELS)
MODELS=""
for (( i = 0; i < $TOP; i++ )); do
  MODELS="$MODELS ${TMP[$i]}"
done
# MODELS=($MODELS)
echo "TOP3 models are : "$MODELS

python $P/average.py -m $MODELS -o model_revo_amun.avg.npz

tar zcvf TMP_MODEL.tar.gz model_revo_amun.avg.npz vocab* valid* $BPE
