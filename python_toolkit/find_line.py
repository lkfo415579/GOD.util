#!/usr/bin/env python
# -*- coding: utf8 -*-
#find file
#print "Author: REVo, 12/22/2017,gm0648@hotmail.com"
import sys,os
reload(sys)
sys.setdefaultencoding('utf-8')
#
import codecs
#
if (len(sys.argv) < 2):
    print "usage: python super_tokenizer.py source_file target_file > output_file"
    sys.exit()#


if __name__ == '__main__':
    #sys.stdin = codecs.getreader('utf-8')(sys.stdin)
    source_file = codecs.open(sys.argv[1],'rb')
    target_file = codecs.open(sys.argv[2],'rb')
    target_corpus = target_file.readlines()
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

    for line in source_file:
        pos = line.find(":")
        line_number = int(line[:pos]) - 1
        target_line = target_corpus[line_number]
        sys.stdout.write(target_line.strip()+'\n')
