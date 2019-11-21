import sys

data = open(sys.argv[1], 'r').readlines()

corpus = {}

for l in data:
    corpus[l] = 1

for key in corpus:
    print(key, end="")
