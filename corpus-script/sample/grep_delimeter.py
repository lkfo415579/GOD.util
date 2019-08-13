# -*- coding: utf-8 -*-
import codecs
import sys

print "usage: python .py source delimiter=|||"
source = codecs.open(sys.argv[1], 'r')
source_out = codecs.open(sys.argv[1] + '.s', 'w')
target_out = codecs.open(sys.argv[1] + '.t', 'w')

if len(sys.argv) > 2:
    d = sys.argv[2]
else:
    d = " ||| "

line_num = 0
for l in source:
    line_num += 1
    l2 = l.strip().split(d)
    if len(l2) == 2:
        source_out.write(l2[0] + '\n')
        target_out.write(l2[1] + '\n')

