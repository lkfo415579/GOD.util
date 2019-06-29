import numpy as np
import yaml
import sys
from sys import getsizeof

new_model_dict = {}
model = np.load(sys.argv[1])

print "Converting MARIAN MODEL 2 old MODEL"
print "LOADED model:%s" % sys.argv[1]

all_s = 0
for key in model:
    print "=" * 100
    #
    name = key
    shape = model[key].shape
    values = model[key]
    print "Name:", name,
    print "Shapes:", shape,
    s = getsizeof(values)
    print "Size:", s, "," + str(s / 1024 ** 2) + "MB"
    if name.find("Wt") != -1:
	name = name[:-1]
    	print "ReName:", name
	values = np.transpose(values, (1, 0)).copy()
    new_model_dict[name] = values

np.savez("tmp.npz", **new_model_dict)
