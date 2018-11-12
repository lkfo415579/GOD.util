#!/usr/bin/env python
# -*- coding: utf8 -*-
# mutil processing of tokenizers (en,zh)
#print "Author: REVo, 12/12/2017,gm0648@hotmail.com"
import logging
from jieba_ext import jieba_python
import tokenize
import multiprocessing
import codecs
import sys
import os
reload(sys)
sys.setdefaultencoding('utf-8')

# check it is python or executable file
if sys.argv[0][-3:] == '.py':
    #it is python
    jieba_ext_folder = os.path.dirname(
        os.path.realpath(__file__)) + "/jieba_ext"
else:
    jieba_ext_folder = os.path.dirname(sys.argv[0]) + "/jieba_ext"
    if jieba_ext_folder[0] != '/':
        jieba_ext_folder = os.path.dirname(
            os.path.realpath(__file__)) + "/" + jieba_ext_folder
#print "JIEBA_EXT:",jieba_ext_folder

#
#

if (len(sys.argv) < 2):
    print "-l : turn on the lowercase the english letters. [False]"
    print "en|zh : language your are tokenizing."
    print "usage: python super_tokenizer.py (en|zh) [-l] [NUM_processes] < input"
    sys.exit()

#
try:
    if sys.argv[2] == '-l':
        lowercase = True
    else:
        lowercase = False
except BaseException:
    lowercase = False
#
if sys.argv[1] != 'en':
    lang = 'zh'
    index_of_muti = 2
    tokenizer = jieba_python.JIE_Tokenizer(jieba_ext_folder)
else:
    lang = 'en'
    index_of_muti = 3
    options = {'lowercase': lowercase, 'moses_escape': True}
    tokenizer = tokenize.Tokenizer(options)
#
try:
    totoal_cpu = int(sys.argv[index_of_muti])
except BaseException:
    totoal_cpu = multiprocessing.cpu_count()
#
logging.critical("Starting processes:%d" % totoal_cpu)


def tokenize(sentence):
    return tokenizer.tokenize(sentence)


def batch_tokenize_process(source_list):
    tmp_sentences = []
    tmp_index = [ele[0] for ele in source_list]
    for index, ele in enumerate(source_list):
        sentence = ele[1]
        #print sentence
        tmp_sentences.append(tokenize(sentence).strip() + "\n")
    return tmp_index, tmp_sentences


if __name__ == '__main__':
    sys.stdin = codecs.getreader('utf-8')(sys.stdin)
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

    SIZE = 500000
    BATCH = 0
    BREAK = True
    while(BREAK):
        logging.critical("BATCH:" + str(BATCH))
        BATCH += 1
        #
        source = []
        for _ in xrange(SIZE):
            line = sys.stdin.readline()
            if not line:
                BREAK = False
                break
            line = str(line).strip()
            source.append(line)
        #
        for index, sen in enumerate(source):
            source[index] = (index, sen)
        # generate multiprocessing data
        privot = len(source) / totoal_cpu
        source_list = [None] * totoal_cpu
        for cpu_id in range(0, totoal_cpu - 1):
            source_list[cpu_id] = source[cpu_id * privot:(cpu_id + 1) * privot]
        source_list[-1] = source[(totoal_cpu - 1) * privot:]
        #
        p = multiprocessing.Pool(processes=totoal_cpu)
        result = p.map(batch_tokenize_process, source_list)
        p.close()
        logging.critical("Finished One BATCH")
        # write files
        #final_sentences = []
        final_tuple = []
        for process_data in result:
            for index, index_sent in enumerate(process_data[0]):
                final_tuple.append((index_sent, process_data[1][index]))
        # resort all sentence by id
        final_tuple = sorted(final_tuple, key=lambda x: x[0])
        for TUPLE in final_tuple:
            sys.stdout.write(TUPLE[1])
        # sys.exit()
        #print final_sentences[480:520]
            # tuple(index_list,sentences),they are sorted already
            # for sentence in process_data[1]:
            #    sys.stdout.write(sentence)
        # DONE one BATCH
