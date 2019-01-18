# -*- coding: utf-8 -*-
import codecs
import sys
from regex import Regex
reload(sys)
sys.setdefaultencoding('utf-8')

sys.stdin = codecs.getreader('UTF-8')(sys.stdin)
sys.stdout = codecs.getwriter('UTF-8')(sys.stdout)


def replacement(line, symbol=".", repl="。"):
    dot = Regex(r'(\D\s*)\%s(\s*[\D$])' % symbol)
    m = dot.findall(line)
    if m:
        for ele in m:
            # consecutive dot avoid
            if symbol != ele[1].strip() and symbol != ele[0].strip():
                # print "BEFORE:", line
                line = line.replace(ele[0] + symbol + ele[1], ele[0] + repl + ele[1])
                # print "AFTER:", line
                # print ele
    return line

for line in sys.stdin:
    line = line.strip()
    line = replacement(line)
    line = replacement(line, ",", "，")
    sys.stdout.write(line + "\n")
