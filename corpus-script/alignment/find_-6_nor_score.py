import sys
# .py tmp2.enzh

errors = {}
r = 0
for l in sys.stdin:
    align, score = l.split(" ||| ")
    score = score.strip()
    align = align.split()
    length_al = float(len(align))
    length_al = length_al if length_al else 1.
    final = float(score) / length_al
    if final < -6.:
        # print (r, score, length_al, final)
        errors[r] = (score, length_al, final)
    r += 1

data = open(sys.argv[1], 'r').readlines()

for e in errors:
    print(data[e])
