# -*- encoding=utf-8 -*-
import codecs
import sys

input = codecs.open(sys.argv[1], 'r')

symbols = ["。", "？"]

def spliting(s):
    for sym in symbols:
        s = s.replace(sym, sym + "\n")
    return s


num = 0
for line in input:
    line = line.strip()
    if line == '=' * 100 or line[:4] == 'http' or line == "":
        continue
    line = spliting(line)
    print(line),
    num += 1

