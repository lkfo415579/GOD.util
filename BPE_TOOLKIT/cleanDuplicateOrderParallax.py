# -*- encoding: utf-8 -*-
import sys
import os
import time
import codecs

from collections import OrderedDict

if len(sys.argv) != 3:
    print 'This program only design for two separated files'
    print 'Input: source, target parallax corpus'
    print 'Output: unique source, target parallax corpus (*.uni file)\n\n'
    print 'Usage: python', sys.argv[0], "[input_source] [input_target]"
    exit()

inputFile_s = sys.argv[1]
inputFile_t = sys.argv[2]
outputFile_s = inputFile_s + '.uni'
outputFile_t = inputFile_t + '.uni'
startTime = time.time()
count = 0

fr_s = codecs.open(inputFile_s, 'r', encoding='utf-8')
fr_t = codecs.open(inputFile_t, 'r', encoding='utf-8')
fw_s = codecs.open(outputFile_s, 'w', encoding='utf-8')
fw_t = codecs.open(outputFile_t, 'w', encoding='utf-8')

file_list = [fr_s, fr_t, fw_s, fw_t]

# refrom the input and store into set
print 'Loading corpus into memory...'
inputList = []
while True:
    s = fr_s.readline()
    t = fr_t.readline()

    if not s or not t:
        break
    count += 1
    if count % 10000 == 0:
        sys.stdout.write('%d\r' % count)
        sys.stdout.flush()

    tmp = s.strip() + ' ||||| ' + t.strip()

    inputList.append(tmp)

print 'Cleaning...'
outputList = list(OrderedDict.fromkeys(inputList))

print 'Exporting result...'
for line in outputList:
    sep = line.split(' ||||| ')
    fw_s.write(sep[0] + '\n')
    fw_t.write(sep[1] + '\n')

for f in file_list:
    f.close()

print 'End with', time.time() - startTime, 'seconds.'
