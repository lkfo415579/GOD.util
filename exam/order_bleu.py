import sacrebleu
import sys
import os

source = open(sys.argv[1], 'r').readlines()
refs = open(sys.argv[2], 'r').readlines()
sys_f = open(sys.argv[3], 'r').readlines()

print("Usage: .py source ref sys_f")
sacrebleu.DEFAULT_TOKENIZER = 'zh'
print(sacrebleu.DEFAULT_TOKENIZER)

data = []
for i, ref_line in enumerate(refs):
    # sys_f[i] = sys_f[i].strip()
    # refs[i] = refs[i].strip()
    # print(refs[i], "#", sys_f[i])
    bleu = sacrebleu.corpus_bleu([sys_f[i]], [[ref_line]], tokenize='zh')
    # print(i, bleu.score)
    data.append((bleu.score, source[i], refs[i], sys_f[i]))

data.sort(reverse=True)

print(data[:50])
folder = 'sort/'
source_out = open(folder + os.path.basename(sys.argv[1]), 'w')
refs_out = open(folder + os.path.basename(sys.argv[2]), 'w')
sys_f_out = open(folder + os.path.basename(sys.argv[3]), 'w')
bleu_out = open(folder + os.path.basename(sys.argv[1]) + '.bleu', 'w')

for d in data:
  s, source, ref, sys_line = d
  refs_out.write(ref)
  sys_f_out.write(sys_line)
  source_out.write(source)
  bleu_out.write(str(s) + '\n')