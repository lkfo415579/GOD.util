# !/usr/bin/env python
# -*- coding: utf8 -*-

import libpytip as pytip
import sys
import codecs
reload(sys)
sys.setdefaultencoding('utf-8')
# pytip.las_tokenize(["abc"])


class Las_Tokenizer(object):
    """docstring for Las_Tokenizer."""
    def __init__(self, model_path):
        pytip.init(model_path)

    def tokenize(self, sentence):
        return pytip.las_tokenize(str(sentence))


if __name__ == '__main__':
    sys.stdin = codecs.getreader('utf-8')(sys.stdin)
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
    PYTIP = Las_Tokenizer(sys.argv[1])

    for sent in sys.stdin:
        result = PYTIP.tokenize(sent)
        sys.stdout.write(result.strip()+"\n")
