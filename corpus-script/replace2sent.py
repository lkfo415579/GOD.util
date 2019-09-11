# -*- coding: utf-8 -*-
import uniout
import codecs
import sys
from regex import Regex
reload(sys)
sys.setdefaultencoding('utf-8')

# sys.stdin = codecs.getreader('UTF-8')(sys.stdin)
src = codecs.open(sys.argv[1], "r").readlines()
tgt = codecs.open(sys.argv[2], "r").readlines()
tgt_o = codecs.open(sys.argv[2] + ".out", "w")
# sys.stdout = codecs.getwriter('UTF-8')(sys.stdout)

replace_items = {"你好": "Hello"}
for k,v in replace_items.iteritems():
    print k, "=>", v

def is_ascii(s):
    return all(ord(c) < 128 for c in s)

r = 0
num_replaced = 0
for line in src:
    line = line.strip()
    t = replace_items.get(line, "")
    if t:
        # found sent need to be replaced
        tgt_o.write(t.strip() + "\n")
        num_replaced += 1
    else:
        tgt_o.write(tgt[r].strip() + "\n")
    r += 1

print "Total replaced :%d" % num_replaced
