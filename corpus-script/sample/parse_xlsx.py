# -*- encoding=utf-8 -*-
from openpyxl import load_workbook
import codecs
import sys

print "usage: .py file"
out = codecs.open(sys.argv[1] + ".src", "w", encoding='utf-8')
out_t = codecs.open(sys.argv[1] + ".tgt", "w", encoding='utf-8')
wb = load_workbook(sys.argv[1])
ws = wb.active

r = 0
for row in ws.rows:
    # check one row data
    # for cell in row:
    #     print cell.value,
    # output A1 and B2
    a = unicode(row[0].value).replace("\n", "")
    b = unicode(row[1].value).replace("\n", "")
    if a == "None" or b == "None":
        print a, b
        continue

    if r % 10000 == 0:
        print "...%d" % r,
    out.write(a + "\n")
    out_t.write(b + "\n")
    r += 1
