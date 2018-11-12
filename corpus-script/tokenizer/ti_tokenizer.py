# -*- coding: utf-8 -*-
from pythainlp.tokenize import word_tokenize
import codecs
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

sys.stdin = codecs.getreader('UTF-8')(sys.stdin)
sys.stdout = codecs.getwriter('UTF-8')(sys.stdout)
if len(sys.argv) > 1 and sys.argv[1] == '-h':
    print "python ti_tokenizer.py filename > output"
    sys.exit()

# main
for line in sys.stdin.readlines():
    line = line.strip()
    line = word_tokenize(line, engine='icu')
    line = " ".join(line)
    sys.stdout.write(line + "\n")
