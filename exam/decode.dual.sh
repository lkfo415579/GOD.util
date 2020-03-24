F=model_revo.npz
M1=DEEP_12L_SSRU_zhen
M2=NEW_BASE_zhen
M3=DEEP_20L_zhen
ALL_MODEL="$M1/$F $M2/$F $M3/$F"
SRCL=zh
TGTL=en
cat $1 | ~/marian-dev/build/marian-decoder -m $ALL_MODEL -v $M1/vocab.$SRCL.yml $M1/vocab.$TGTL.yml -b 8 --mini-batch 60 \
-d $2 -o output.txt --maxi-batch 10 --max-length 150 --max-length-crop --n-best --quiet-translation
