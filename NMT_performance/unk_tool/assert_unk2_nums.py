# -*- coding: utf-8 -*-
import codecs
import sys

sys.stdin = codecs.getreader('UTF-8')(sys.stdin).readlines()
sys.stdout = codecs.getwriter('UTF-8')(sys.stdout)

c = 0
for i in range(0, len(sys.stdin), 2):
    l1 = sys.stdin[i].strip()
    l2 = sys.stdin[i + 1].strip()
    if l1.count("<unk2>") != l2.count("<unk2>"):
        c += 1
    else:
        # same nums
        #
        # one of them is single unk2 tag
        # check if the oppsite is extractly the same
        if l1 == "<unk2>":
            if l2 != "<unk2>":
                continue
        if l2 == "<unk2>":
            if l1 != "<unk2>":
                continue
        sys.stdout.write(l1 + '\n')
        sys.stdout.write(l2 + '\n')
