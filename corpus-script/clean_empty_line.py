# -*- coding: utf-8 -*-
# python3
import codecs
import sys

c = 0
while(1):
    try:
        line = sys.stdin.readline()
        if not line:
            break
    except:
        continue
    # print ("C:", c)
    c += 1
    if line.strip() != '':
        sys.stdout.write(str(line))
