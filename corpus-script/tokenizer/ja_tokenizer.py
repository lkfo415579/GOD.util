# -*- coding: utf-8 -*-
import MeCab
import codecs
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

sys.stdin = codecs.getreader('UTF-8')(sys.stdin)
sys.stdout = codecs.getwriter('UTF-8')(sys.stdout)
# if sys.argv[1] == '-h':
#     print "python ja_tokenizer.py filename > output"

mecab_ko = MeCab.Tagger("-O wakati".encode("utf-8"))
# main
# file = sys.stdin
# f_ko = codecs.open(file, 'r').readlines()

for line in sys.stdin:
    line = line.strip()
    line = mecab_ko.parse(line.encode("utf-8")).decode('utf8').strip()
    sys.stdout.write(line + "\n")
