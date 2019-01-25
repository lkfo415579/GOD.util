# -*- encoding=utf-8
import codecs
import sys

ctx = codecs.getreader("utf-8")(sys.stdin)

src_f = codecs.open("train.src", "w", encoding="utf-8")
tgt_f = codecs.open("train.tgt", "w", encoding="utf-8")
ctx_f = codecs.open("train.ctx", "w", encoding="utf-8")

# only select top 5 of previous sents
k = 5
cur_doc_id = 0
doc_saver = []
for ctx_id, line in enumerate(ctx):
    try:
        doc_id, id, src, tgt = line.split("\t")
    except ValueError:
        # need more 1
        # skip
        continue
    tgt = tgt.strip()
    if doc_id.isdigit():
        # print doc_id, id, src, tgt
        # switch to new doc
        if cur_doc_id != doc_id:
            cur_doc_id = doc_id
            doc_saver = []
        src_f.write(src + "\n")
        tgt_f.write(tgt + "\n")
        ctx_f.write(" ".join(doc_saver) + "\n")
        if len(doc_saver) == k:
            del doc_saver[0]
        doc_saver.append(src)
