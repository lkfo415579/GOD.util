# -*- coding: utf-8 -*-
import codecs
import sys

sys.stdin = codecs.getreader('UTF-8')(sys.stdin).readlines()
sys.stdout = codecs.getwriter('UTF-8')(sys.stdout)

c = 0
for i in range(0, len(sys.stdin), 2):
    l = sys.stdin[i]
    l2 = sys.stdin[i + 1]
    if l.count("<unk2>") != l2.count("<unk2>"):
        c += 1
    else:
        sys.stdout.write(l.strip() + '\n')
        sys.stdout.write(l2.strip() + '\n')
