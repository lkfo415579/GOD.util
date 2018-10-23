# -*- coding: utf-8 -*-
import codecs
import sys

if len(sys.argv) < 2:
    print "Usage : python %s" % sys.argv[0], " source target len_factor=2"
if len(sys.argv) < 3:
    len_factor = float(sys.argv[3])
else:
    len_factor = 2

f1 = codecs.open(sys.argv[1], 'r', encoding='utf8').readlines()
f2 = codecs.open(sys.argv[2], 'r', encoding='utf8').readlines()

print "Finished Reading"

f1_out = codecs.open(sys.argv[1] + ".clean", 'wa', encoding='utf8')
f2_out = codecs.open(sys.argv[2] + ".clean", 'wa', encoding='utf8')
err = 0
for index, line in enumerate(f1):
    line2 = f2[index]
    if len(line) < len_factor * len(line2) and len(line2) < len_factor * len(line):
        f1_out.write(line.strip() + '\n')
        f2_out.write(line2.strip() + '\n')
    else:
        err += 1

print "total err sents : %d" % err
