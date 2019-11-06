# -*- coding: utf-8 -*-
import codecs
import kenlm
import sys
sys.stdin = codecs.getreader('UTF-8')(sys.stdin)
sys.stdout = codecs.getwriter('UTF-8')(sys.stdout)
# usage python .py model threahold
model = kenlm.Model(sys.argv[1])
threadhold = -5.0 if len(sys.argv[2]) < 2 else float(sys.argv[2])
id = 0
for line in sys.stdin:
    line = line.strip()
    lm_score = model.score(line, bos=True, eos=True)
    num_tokens = float(len(line.split()))
    # math
    nor_score = float(lm_score / float(num_tokens))
    perplexity = 1. / (10. ** (lm_score / num_tokens))
    #
    if nor_score <= threadhold:
        print ("%f ||| %f ||| %d ||| %s" % (perplexity, nor_score, id, line))
    id += 1
    # sys.stdout.write(" ".join(line) + "\n")
