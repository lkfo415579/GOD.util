# -*- coding: utf-8 -*-
import codecs
import sys

sys.stdin = codecs.getreader('UTF-8')(sys.stdin)
sys.stdout = codecs.getwriter('UTF-8')(sys.stdout)

pos = int(sys.argv[1])
if len(sys.argv) > 2:
    d = sys.argv[2]
else:
    d = " ||| "

for l in sys.stdin:
    l2 = l.strip()
    sys.stdout.write(l2.split(d)[pos] + '\n')
