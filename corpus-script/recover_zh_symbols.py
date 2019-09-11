# -*- coding: utf-8 -*-
import codecs
import sys
from regex import Regex
reload(sys)
sys.setdefaultencoding('utf-8')

sys.stdin = codecs.getreader('UTF-8')(sys.stdin)
sys.stdout = codecs.getwriter('UTF-8')(sys.stdout)


def is_ascii(s):
    return all(ord(c) < 128 for c in s)

def replacement(line, symbol=".", repl="。"):
    line = line.replace(". . .", ".")
    line = line.replace(u"．", ".")
    # line = line.replace("...", ".")
    dot = Regex(r'(\S\s*)\%s(\s*\S*)' % symbol)
    m = dot.findall(line)
    if m:
        # print "BEFORE:", line
        # print m
        for ele in m:
            b_char = ele[0].strip()
            a_char = ele[1].strip()
            # consecutive dot avoid
            if symbol != b_char and symbol != a_char:
                # both are digit or are letters
                if is_ascii(b_char) and is_ascii(a_char):
                    return line
                line = line.replace(ele[0] + symbol + ele[1], ele[0] + repl + ele[1])
                # debug
                # if symbol == ',':
                #     print m
                #     print "AFTER:", line
    return line

tail_dot = Regex(r'\.+$')
def remove_tailing_dot(line):
    return tail_dot.sub("", line)

for line in sys.stdin:
    line = line.strip()
    line = replacement(line)
    line = replacement(line, ",", "，")
    line = remove_tailing_dot(line)
    sys.stdout.write(line + "\n")
