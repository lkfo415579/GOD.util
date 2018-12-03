# -*- coding: utf-8 -*-
import codecs
import sys

syms = [",", "(", ")", "%", "-"]


def isfloat(line):
    for sym in syms:
        line = line.replace(sym, "")
    try:
        f = float(line)
        return True
    except:
        return False
        pass


c = 0
while(1):
    try:
        line = sys.stdin.readline()
        if not line:
            break
    except BaseException:
        continue
    #
    c += 1
    # 1. not empty line
    # 2. not single digit
    # 3. clean mutiple space
    # 4. not single -
    line = line.strip()
    line = line.replace("	", " ")
    line = line.replace("  ", " ")
    line = line.replace("  ", " ")
    if line != '' and not isfloat(line) and line != '-':
        sys.stdout.write(str(line) + '\n')
