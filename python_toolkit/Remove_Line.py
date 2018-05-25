# -*- coding:utf-8 -*-
'''
Created on 2016年3月28日

@author: Peter Hao Zong
'''
import codecs
import sys
def remove_line(filename):
    source_file = codecs.open(filename,'r','utf8')
    lines = source_file.read().split('\n')
    outfile = codecs.open(filename + '.without_external_line','w','utf8')
    for line in lines:
        wrtstr = ''
        for l in line.splitlines():
            wrtstr += l + ' '
        outfile.write(wrtstr + '\n')

if __name__ == '__main__':
    argv = sys.argv[1]
    remove_line(argv)
