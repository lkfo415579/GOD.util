# -*- coding: utf-8 -*-
import codecs
import sys

if len(sys.argv) < 2:
    print "Usage : python %s" % sys.argv[0], " source target len_factor=2 source_style=0[0=count_space, 1=not counting_space] target_style=1[0=count_space, 1=not counting_space]"
if len(sys.argv) == 4:
    len_factor = float(sys.argv[3])
    print "LEN_FACTOR:%f" % len_factor
else:
    len_factor = 2
# count space option
s_count = 1
t_count = 1
if len(sys.argv) > 4:
    s_count = int(sys.argv[4])
    t_count = int(sys.argv[5])
# display parameter
print "S_count:%d, T_count:%d" % (s_count, t_count)
f1 = codecs.open(sys.argv[1], 'r', encoding='utf8').readlines()
f2 = codecs.open(sys.argv[2], 'r', encoding='utf8').readlines()

print "Finished Reading"

f1_out = codecs.open(sys.argv[1] + ".double", 'wa', encoding='utf8')
f2_out = codecs.open(sys.argv[2] + ".double", 'wa', encoding='utf8')
err_out = codecs.open(sys.argv[1] + ".err", 'wa', encoding='utf8')

err = 0
for index, line in enumerate(f1):
    line2 = f2[index].strip()
    line = line.strip()
    # count space or not
    if s_count:
        s_len = len(line.split())
    else:
        s_len = len(line)
    if t_count:
        t_len = len(line2.split())
    else:
        t_len = len(line2)
    #
    larger = max(s_len, t_len)
    smaller = min(s_len, t_len)
    if larger - smaller <= smaller * len_factor:
        f1_out.write(line + '\n')
        f2_out.write(line2 + '\n')
    else:
        err += 1
        err_out.write(line + " ||| " + line2 + " ||| %d-%d" % (s_len, t_len)  +'\n')
        # debug
    #     print t_len
    #     print '---'
    #     print line
    #     print line2
    # # debug
    # if err > 10:
    #     break

print "total err sents : %d" % err
