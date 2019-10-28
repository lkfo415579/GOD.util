# -*- encoding=utf-8 -*-
import codecs
import sys

input = codecs.open(sys.argv[1], 'r', encoding='utf-8')

num = 0
MAX = 200
for line in input:
    words = line.strip().split()
    if len(words) > MAX:
        continue
    print (line.strip())
