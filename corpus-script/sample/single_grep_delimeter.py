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

line_num = 0
for l in sys.stdin:
    line_num += 1
    l2 = l.strip()
    try:
        sys.stdout.write(l2.split(d)[pos] + '\n')
    except:
        # print "Fucked in line:%d" % line_num
        # break
        pass


