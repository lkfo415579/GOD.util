import codecs
import sys
import os
import subprocess

# sys.stdout = codecs.getwriter("UTF-8")(sys.stdout)
# SED methods
errors = codecs.open(sys.argv[1], "r", encoding='utf8').readlines()
# errors = errors[:100]
# s = "'"
# for e in errors:
#     e = e.split(':')[0]
#     s += "%sd;" % e
# s += "'"
# print s
# 
# os.system("sed -e %s %s" % (s, sys.argv[2]))

# readall methods
E = []
for e in errors:
    e = int(e.split(':')[0])
    E.append(e)
big_data = open(sys.argv[2], 'r', encoding='utf8', errors='ignore').readlines()

E.sort(reverse=False)
print(len(E))
print(len(big_data))
res = []
r = 0
for e in E:
    if r != e:
        print(r, e)
        res += big_data[r:e]
    r = e + 1

res += big_data[r:]
print(len(res))
# for l in res:
#     print(l, end="")
