import sys
import yaml

for i in sys.argv[1:]:
    f = open(i + "/valid.log", 'r').readlines()
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
    other = 'maxi-batch: %s' % y['maxi-batch']
    print(i, b[0], other)



