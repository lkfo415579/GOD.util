VALID=dev/newstest2017-zhen-src.pre.zh
cat $1 | ~/competence/build/marian-decoder -c $2/model_revo.npz.decoder.yml -b 12 -n 1.0 --mini-batch 10 -d $3 -o \
output/final_exam.txt

cat output/final_exam.txt | sed 's/@@ //g' | python ~/GOD.util/util_token/detokenize.py -l zh -m \
    | sacrebleu -tok zh $VALID
