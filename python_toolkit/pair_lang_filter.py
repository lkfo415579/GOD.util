#!/usr/bin/env python
# -*- coding: utf8 -*-
#v1.1 revo,12/15/2017 , fix last batch duplicated problem.
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
#from langdetect import detect
#import pycld2 as cld2
from polyglot.detect import Detector
import codecs
import time
import os
from multiprocessing import Process,Pool
import multiprocessing
import logging
logging.basicConfig(level=logging.ERROR)
print "VERSION1.2, 12/15/2017"
if (sys.argv[1] == '-h'):
    print "usage: python pair_lang_filter.py valid.General.en-zh zh en valid.output.en-zh 4"
    sys.exit()
s_lang = sys.argv[2]
t_lang = sys.argv[3]
output_s = codecs.open(sys.argv[4]+"."+s_lang,"wa")
output_t = codecs.open(sys.argv[4]+"."+t_lang,"wa")

try:
    if len(sys.argv[5]) > 0:
        totoal_cpu = int(sys.argv[5])
except:
    totoal_cpu = multiprocessing.cpu_count()
print "TOTAL CPU :%d" % totoal_cpu

SIZE = 500000
#SIZE = 500
EPOCH = 1


source_file_P = codecs.open(sys.argv[1]+"."+s_lang,"rb")
target_file_P = codecs.open(sys.argv[1]+"."+t_lang,"rb")


while(True):
    print "Reading Corpus,EPOCH %d" % EPOCH
    source = []
    target = []

    for _ in xrange(SIZE):
        line = source_file_P.readline()
        line_tar = target_file_P.readline()
        source.append(line)
        target.append(line_tar)
    print "LLEEEEEN:%d" % len(source)
    if source == target:
        break
    for index,sen in enumerate(source):
        source[index] = (index,sen)





    #if len(source) != len(target):
    #    assert ("FUCKED, two files are not having the same line number")

    print "Split corpus into different CPU"
    privot = len(source) / totoal_cpu
    source_list = [None] * totoal_cpu
    #target_list = [None] * totoal_cpu
    for cpu_id in range(0,totoal_cpu-1):
        source_list[cpu_id] = source[cpu_id*privot:(cpu_id+1)*privot]
        #target_list[cpu_id] = target[cpu_id*privot:(cpu_id+1)*privot]
    source_list[-1] = source[(totoal_cpu-1)*privot:]
    #target_list[-1] = target[cpu_id*privot:]
    print "PRIVOT:%d" % privot
    print "Start finding different lang"


    def find_error(source):
        delete_list = []
        t0 = time.time()
        found = 0
        proc_name = multiprocessing.current_process().name
        #print "@@@@@@@@@@@@@@@@@@@@@"*4
        #print "Current process:%s" % proc_name

        for runner,two in enumerate(source):
            index = two[0]
            sentence = two[1]
            if runner % 1000 == 0:
                t1 = time.time()
                sys.stdout.write("PROC:"+proc_name+",Line:"+str(runner)+",Time Cost:"+str(1000.0/(t1-t0))+"lines/s\r")
                t0 = t1
                sys.stdout.flush()
            tmp_s = sentence.decode('utf8')
            #
            #detected = Detector(tmp_s).language.code[:2]
            #print detected
            try:
                detected = Detector(tmp_s).language.code[:2]
                if detected == t_lang:
                    #print "INDEX:%d,%s" % (index,sentence)
                    #print detected
                    delete_list.append(index)
                    found += 1
            except:
                pass

        #print "%%%%%%%%%%%%%%%%%%%%%%%%"
        #print "Found ERROR sentences : %d" % found

        return delete_list,found


    p = Pool(processes=totoal_cpu)
    result = p.map(find_error,source_list)
    p.close()
    #############FINISHED calculating##############
    DELETE = []
    FOUND = 0

    for ele in result:
        DELETE += ele[0]
        FOUND += ele[1]
    DELETE.sort()
    print DELETE[:5]
    print "Totol ERROR sentences : %d " % FOUND
    #del source
    #del source_list

    for ele in source:
        if ele[0] not in DELETE:
            output_s.write(ele[1])
            output_t.write(target[ele[0]])


    ###
    EPOCH+= 1
print "DONE!!!"
