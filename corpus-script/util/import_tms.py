import sqlite3
import codecs
import sys

conn = sqlite3.connect("mt.db")
glossary_f = codecs.open(sys.argv[1], encoding="utf-8").readlines()

srcl = 'en'
tgtl = 'zh'
query = "INSERT INTO tms (term, translation, srcl, tgtl) values (?,?,?,?)"

for i, sent in enumerate(glossary_f):
    if i % 2 == 0:
        sent_next = glossary_f[i + 1]
        conn.execute(query, (sent, sent_next, srcl, tgtl))
conn.commit()
