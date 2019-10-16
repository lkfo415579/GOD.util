dev_output=18/wmt18.enzh.bpe.en.output
dev=18/wmt18.enzh.bpe.zh
ref=19/wmt19.bpe.en

mkdir -p workshop
# training
python3 kenlm_scorer.py final_mono.binary < $dev_output > workshop/dev.F
python train.py --nbest workshop/dev.F --ref $dev --working-dir rescore-work --bin-dir ~/NMT/mosesdecoder-master/bin
python rescore.py rescore-work/rescore.ini < workshop/dev.F | python topbest.py | sed 's/@@ //g' | python ~/GOD.util/util_token/detokenize.py -l zh -m > workshop/dev.topbest.detok
echo "WMT18(dev)"
cat workshop/dev.topbest.detok | sacrebleu -t wmt18 -l en-zh
# testing
python3 kenlm_scorer.py final_mono.binary < $ref.output > workshop/ref.F
python rescore.py rescore-work/rescore.ini < workshop/ref.F > workshop/ref.rescore
python topbest.py < workshop/ref.rescore > workshop/ref.topbest
cat workshop/ref.topbest | sed 's/@@ //g' | python ~/GOD.util/util_token/detokenize.py -l zh -m > workshop/ref.topbest.detok
# BLEU
# ~/GOD.util/exam/multi-bleu.perl -lc wmt18.enzh.bpe.zh < output.topbest
echo "WMT19(test)"
cat workshop/ref.topbest.detok | sacrebleu -t wmt19 -l en-zh
echo "Pure Decoding WMT19"
python topbest.py < $ref.output | sed 's/@@ //g' | python ~/GOD.util/util_token/detokenize.py -l zh -m | sacrebleu -t wmt19 -l en-zh
