# -*- coding: utf-8 -*-
import MeCab
import codecs
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

sys.stdout = codecs.getwriter('UTF-8')(sys.stdout)
if sys.argv[1] == '-h':
    print "python ja_tokenizer.py filename > output"

mecab_ko = MeCab.Tagger("-O wakati".encode("utf-8"))
# main
file = sys.argv[1]
f_ko = codecs.open(file, 'r').readlines()

for line in f_ko:
    line = line.strip()
    line = mecab_ko.parse(line.encode("utf-8")).decode('utf8').strip()
    sys.stdout.write(line + "\n")
