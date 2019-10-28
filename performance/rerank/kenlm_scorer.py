# -*- coding: utf-8 -*-
import codecs
import kenlm
import pkuseg
import sys
# sys.stdin = codecs.getreader('UTF-8')(sys.stdin)
# sys.stdout = codecs.getwriter('UTF-8')(sys.stdout)
# usage python .py model threahold
pkuseg = pkuseg.pkuseg(model_name='news')
model = kenlm.Model(sys.argv[1])
pre_id = 0
for line in sys.stdin:
    line = line.strip().split(" ||| ")
    # COMMON VAR
    word_num = float(len(line[1].split()))
    word_num = word_num if word_num else 1.
    res = ""
    for i, ele in enumerate(line):
        if i == 2:
            pass
            # LM features
            # sent = line[1].replace("@@ ", "").replace(" ", "")
            # words = pkuseg.cut(sent)
            # sent = " ".join(words)
            # lm_score = model.score(sent, bos=True, eos=True)
            # ppl = 1. / (10. ** (lm_score / word_num))
            # ele += " LM= %f %f" % (lm_score, ppl)
            # # ele += " LM= %f" % (lm_score)
            # # word count features
            # ele += " CHAR_COUNT= %f %f" % (len(line[1]), word_num)
            # length-normalized score
            # ext_features = ele.split()
            # MT_scores = float(ext_features[1]) + float(ext_features[3])
            # ele += " LENGTH_NOR= %f" % MT_scores 
        if i == 3:
            continue
        res += ele + " ||| " if i != len(line) - 1 else ele
    print (res)
