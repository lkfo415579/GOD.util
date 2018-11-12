#!/usr/bin/python
# -*- coding: utf-8 -*-
import codecs
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

if sys.argv[1] == '-h':
    print "Usage: python *.py [source_file] [trans_file] > output"

source_file = codecs.open(sys.argv[1], 'rb')
trans_file = codecs.open(sys.argv[2], 'rb')
sys.stdout = codecs.getwriter('UTF-8')(sys.stdout)


def find_unk(line, UNK="<unk>"):
    tmp = line.split()
    UNK_POS = []
    for index, word in enumerate(tmp):
        if word == UNK:
            UNK_POS.append(index)
    return UNK_POS


for line in trans_file:
    line, align = line.strip().split("|||")
    align = align.split()
    align = [int(target.split('-')[1]) for target in align]
    UNK_POS = find_unk(line)
    source_line = source_file.readline().split()
    copy_line = line[:]
    line = line.split()

    # print "UNK_POS:", UNK_POS
    # print "line:", " ".join(line)
    # print "Align:", align
    # print source_line
    # print copy_line.find("<unk> <unk>")
    if copy_line.find("<unk> <unk>") == -1:
        for POS in UNK_POS:
            # print "Align[POS]:", align[POS]
            if align[POS] == len(source_line):
                # matched </s>
                line[POS] = ""
            else:
                line[POS] = source_line[align[POS]]
    # print " ".join(line)
    sys.stdout.write(" ".join(line) + "\n")
