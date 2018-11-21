python ~/GOD.util/util_token/tokenize.py -l $1.en $1.en.tok
python ~/GOD.util/BPE_TOOLKIT/apply_bpe.py -c ~/new_gate/en-zh/en.bpe < $1.en.tok > $1.en.bpe
