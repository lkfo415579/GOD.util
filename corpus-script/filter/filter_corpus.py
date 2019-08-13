# -*- encoding=utf-8 -*-
import codecs
import sys
from regex import Regex

print ("Usage: python x.py char_vocab src_file tgt_file")
info = codecs.open(sys.argv[1], 'r', encoding="utf-8").readlines()
src_f = codecs.open(sys.argv[2], 'r', encoding="utf-8").readlines()
tgt_f = codecs.open(sys.argv[3], 'r', encoding="utf-8").readlines()
src_out = codecs.open(sys.argv[2] + ".out", 'w', encoding="utf-8")
tgt_out = codecs.open(sys.argv[3] + ".out", 'w', encoding="utf-8")
# sys.stdin = codecs.getreader('UTF-8')(sys.stdin)
# sys.stdout = codecs.getreader('UTF-8')(sys.stdout)
# core parameter
lang = 'ja'
# Weird char are all in valid unicode range [JP pun, HIRAGANA, KATAKANA, half-width katakana, CJK, ASCII]
unicode_range = Regex(r'[^\u3000-\u303f\u3040-\u309f\u30a0-\u30ff\uff00-\uffef\u4e00-\u9faf\u0020-\u024f]')
# filter by single letter
regular_char_filter = "[\u301c\u226a\u226b\u25c6\u25b2\ufffd\u2606\u25b3\uff64\uff63\uff88\uff78"


def encode_Uni(text):
  t = ""
  for c in text:
    t += 'U+%04x ' % ord(c)
  return t
  
def encode_uni_py(text):
  t = ""
  for c in text:
    t += '\\u%04x' % ord(c)
  return t

# use for output unicode
out_range = 0
for line in info:
  char = line.split(":")[0]
  if char != "":
    found = unicode_range.findall(char)
    # print (char, encode_Uni(char), len(found))
    if len(found):
      regular_char_filter += encode_uni_py(char)
      out_range += 1

print ("Out Range : %d" % out_range)
filter_rule = Regex(r'%s]' % regular_char_filter)
#true hand made filter
error_line = []
for id, line in enumerate(src_f):
  found = filter_rule.findall(line)
  if id % 10000 == 0:
    print ("%d..." % id, end='')
  if found:
    error_line.append(id)
    # print "Line %d is invalid." % id + 1
  else:
    # saved sent
    src_out.write(line.strip() + "\n")
    tgt_out.write(tgt_f[id].strip() + "\n")

print ("\nTotal Error line : %d" % len(error_line))
