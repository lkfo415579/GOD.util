import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
import sys

print("python x.py title valid.log < mod_file")

# BLUE
bleu_f = open(sys.argv[2], 'r').readlines()
bleu = []
for l in bleu_f:
    if l.find('translation') != -1:
        l = l.split()
        step = int(l[7])
        score = float(l[11])
        bleu.append(score)
# BLEU

plt.title(sys.argv[1])

r = 0

data = []
name = []
mod = []
for line in sys.stdin:
    # print (line)
    if r % 2 == 0:
        t = line.split(".")[1][4:]
        name.append(int(t))
    else:
        mod.append(float(line))
    r += 1
for i, n in enumerate(name):
    data.append((n, mod[i]))

data.sort()

print (data)

name = [x[0] for x in data]
mod = [x[1] for x in data]

plt.ylabel("avg mod")
plt.xlabel("step")
plt.plot(name, mod)

ax2_color = 'tab:red'
ax2 = plt.twinx()
ax2.set_ylabel("BLEU SCORE", color=ax2_color)
ax2.plot(name, bleu, color=ax2_color)

plt.locator_params(nbins=20)
plt.show()
