# -*- encoding=utf-8 -*-
import codecs
import sys

print "Usage python find_err_align.py align_file factor=2"
align = codecs.open(sys.argv[1], "r").readlines()
# corpus = codecs.open(sys.argv[2], "r").readlines()
print "Finished reading"

avg = {}
for i, line in enumerate(align):
    score, a = line.split(" ||| ")
    # a = [x.split("-")[1] for x in a.split()]
    score = float(score)
    try:
        avg[len(a)] = (avg[len(a)][0] + score, float(avg[len(a)][1] + 1))
    except KeyError:
        avg[len(a)] = (score, 1.0)

for k in avg:
    avg[k] = (avg[k][0] / avg[k][1], avg[k][1])

print str(avg)[:500]

# find unnatural lines
out = codecs.open("err", 'w')
if len(sys.argv) < 3:
    factor = 2
else:
    factor = float(sys.argv[2])
print "Factor:%f" % factor
#
for i, line in enumerate(align):
    score, a = line.split(" ||| ")
    score = float(score)
    standard = float(avg[len(a)][0] * factor)
    if score < standard:
        info = "%d ||| %f ||| %d ||| %f *%f = %f" % (i, score, len(a), avg[len(a)][0], factor, standard)
        out.write(info + "\n")
print "INDEX starts from 0"
