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
  return [UP_LIST, BLEU_LIST]
    

valid = {}
for i in range(1, len(sys.argv)):
  print "NAME:", sys.argv[i]
  t = codecs.open(sys.argv[i], "r").readlines()
  valid[sys.argv[i]] = parse(t)

plt.title("BLEU Comparation")

for name in valid:
  plt.plot(valid[name][0], valid[name][1], label=name)
  
plt.locator_params(nbins=20)
# plt.xaxis.set_major_locator(MultipleLocator(20))
# plt.yaxis.set_major_locator(MultipleLocator(20))
plt.legend(loc='best')
plt.show()
