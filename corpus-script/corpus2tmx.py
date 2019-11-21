import sys

a = open(sys.argv[1], 'r').readlines()
b = open(sys.argv[2], 'r').readlines()
if len(a) != len(b):
    print("Fucked they are not the same lines")

for i, l in enumerate(a):
    print(l, end="")
    print(b[i], end="")

