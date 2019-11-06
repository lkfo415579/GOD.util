# -*- coding: utf-8 -*-
# import codecs
import pkuseg
import sys
# sys.stdin = codecs.getreader('UTF-8')(sys.stdin)
# sys.stdout = codecs.getwriter('UTF-8')(sys.stdout)
seg = pkuseg.pkuseg(model_name='news')

for line in sys.stdin:
    line = line.strip()
    line = seg.cut(line)
    sys.stdout.write(" ".join(line) + "\n")
