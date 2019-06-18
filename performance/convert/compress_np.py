import numpy as np
import sys
# import uniout

f = open(sys.argv[1], 'r').readlines()

py_str_list = []
for i, line in enumerate(f):
    line = line.strip()
    word, id = line.split(": ")
    if word[0] == '"':
        py_str_list.append(word[1:-1])
    else:
        py_str_list.append(word)

# convert in to numpy
print py_str_list[:20]
data = np.array(py_str_list, dtype='string')

print data[:20]
print data.dtype
print data.shape

np.savez_compressed("vocab.zh", vocab=data)
np.savez("vocab.zh.nor", vocab=data)

# reading
res = np.load("vocab.zh.nor.npz")

print data[:20], data.dtype, data.shape
