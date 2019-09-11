import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import codecs
import sys

def parse(t):
  UP_LIST = []
  BLEU_LIST = []
  for line in t:
    if line.find("translation") != -1:
      p = line.find("Up.")
      line = line[p+3:].split(":")
      UP = int(line[0].replace(" ", ""))
      BLEU = float(line[2].replace(" ", ""))
      # print UP, BLEU
      
      UP_LIST.append(UP)
      BLEU_LIST.append(BLEU)
      # print UP, BLEU
  print "-- BEST BLEU:%d, STEP:%d" % (max(BLEU_LIST), max(UP_LIST))
  return [UP_LIST, BLEU_LIST]
    

valid = {}
for i in range(1, len(sys.argv)):
  # skip non folder
  if sys.argv[i].split("/")[-1].find(".") != -1:
      continue
  print "NAME:", sys.argv[i],
  t = codecs.open(sys.argv[i] + "/valid.log", "r").readlines()
  valid[sys.argv[i]] = parse(t)

plt.figure(figsize=(20, 10))
plt.title("BLEU Comparation")

for name in valid:
  plt.plot(valid[name][0], valid[name][1], label=name)
  
plt.locator_params(nbins=20)
plt.legend(loc='best')
# plt.figure(figsize=(100, 50))
# plt.set_size_inches(100, 50)
# plt.savefig("bleu.png", dpi=300)
plt.savefig("bleu.png")
# plt.show()
