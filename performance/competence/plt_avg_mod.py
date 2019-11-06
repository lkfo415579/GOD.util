import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')

print("python x.py valid.log mod_file")

def draw_bleu(bleu_f, name, plt_name, color):
    bleu = {}
    for l in bleu_f:
        if l.find('translation') != -1:
            l = l.split()
            step = int(l[7])
            score = float(l[11])
            bleu[step] = score
    # follow the name, fit bleu to name
    BLEU = []
    for n in name:
        BLEU.append(bleu[n])
    # BLEU
    BLEU = BLEU[:TOTAL_STEP]
    ax2.plot(name, BLEU, label="BLEU_" + plt_name, color=color)
    print(bleu)
        
def draw(MOD_log, plt_name, color):
    r = 0
    data = []
    name = []
    mod = []
    for line in MOD_log:
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
    data = data[:TOTAL_STEP]
    name = [x[0] for x in data]
    mod = [x[1] for x in data]

    ax1.plot(name, mod, label=plt_name, color=color)
    print(data)
    print("=" * 100)
    return name

TOTAL_STEP = 47
ax1 = plt.figure().add_subplot(111)
ax1.set_ylabel("AVG MOD")
ax2 = plt.twinx()
ax2.set_ylabel("BLEU SCORE")
#
colors = {1:["b", "g"], 3:["r", "c"], 5:["m", "y"]}
names = {1: "CL_MOD", 3: "BASE", 5: "AVG_MOD"}
for i in range(1, len(sys.argv), 2):
    bleu_f = open(sys.argv[i], 'r').readlines()
    MOD_log = open(sys.argv[i + 1], 'r').readlines()
    name = draw(MOD_log, names[i], colors[i][0])
    draw_bleu(bleu_f, name, names[i], colors[i][1])
#
ax1.set_xlabel("STEP")
ax1.legend(loc='best')
ax2.legend(loc='lower right')
plt.title("MOD_AVG + BLEU")
plt.locator_params(nbins=20)
plt.show()
