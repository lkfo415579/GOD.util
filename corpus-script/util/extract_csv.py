import csv
import sys
csv_f = open(sys.argv[1], 'r')

csv_reader = csv.reader(csv_f, delimiter=',')

r = 0
for row in csv_reader:
    if r != 0:
        src, tgt = row[1], row[2]
        print(src.replace("\n", ""))
        print(tgt.replace("\n", ""))
    r += 1
