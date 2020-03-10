import sys
import yaml

MAX = -1
BEST = []
for i in sys.argv[1:]:
    try:
        f = open(i + "/valid.log", 'r').readlines()
    except:
        continue
    b = []
    for l in f:
        if l.find('translation') != -1:
            data = l.split(" : ")
            bleu = data[3].strip()
            bleu = float(bleu)
            b.append((data[1], bleu))
    b.sort(key=lambda x: x[1], reverse=True)
    # get config
    with open(i + '/model_revo.npz.yml', 'r') as f:
        y = yaml.load(f, Loader=yaml.FullLoader)
    other = 'maxi-batch: %s, valid: %s' % (y['maxi-batch'], y['valid-sets'])
    current = i, b[0], other
    print(current)
    if b[0][1] > MAX:
        MAX = b[0][1]
        BEST = current
print("=" * 50 + "BEST" + "=" * 50)
print(BEST) 


