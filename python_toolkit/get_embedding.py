#!/usr/bin/env python

from __future__ import print_function

import os
import sys
import argparse

import numpy as np

# Parse arguments.
parser = argparse.ArgumentParser()
parser.add_argument('-m', '--model', nargs='+', required=True,
                    help="Models to average")
parser.add_argument('-o', '--output', required=True,
                    help="Output path")
args = parser.parse_args()

# *average* holds the model matrix.
average = dict()
# No. of models.
n = len(args.model)

for filename in args.model:
    print("Loading {}".format(filename))
    with open(filename, "rb") as mfile:
        # Loads matrix from model file.
        m = np.load(mfile)
        print ("WEMB:")
        print (m['Wemb'])
        print ("Len:")
        print (len(m['Wemb']))
        print ("Len of single :",len(m['Wemb'][0]))
        output = m['Wemb']
        print ("200:",m['Wemb'][38140:38200])
        for k in m:
            print ("key:",k)

#sys.exit()
# Actual averaging.
# for k in average:
#     if "special" not in k:
#         average[k] /= n

# Save averaged model to file.
print("Saving to {}".format(args.output))
np.savez(args.output, output)
