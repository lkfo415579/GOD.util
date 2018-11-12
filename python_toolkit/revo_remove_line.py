# -*- coding:utf-8 -*-
'''
Created on 2016年3月28日

@author: Peter Hao Zong
'''
import codecs
import sys


def remove_line(filename, out):
    source_file = codecs.open(filename, 'r', 'utf8')
    outfile = codecs.open(out, 'w', 'utf8')
    index = 0
    while(1):
        index += 1
        line = source_file.readline()
        if not line:
            break
        #lines = source_file.read().split('\n')
        wrtstr = ''
        mutilines = line.splitlines()
        if len(mutilines) > 1:
            print "JESUS:", len(mutilines)
            print "INDEX:", index
        for l in mutilines:
            wrtstr += l + ' '
        outfile.write(wrtstr.strip() + '\n')


if __name__ == '__main__':
    argv = sys.argv[1]
    remove_line(argv, sys.argv[2])
