# -*- encoding=utf-8 -*-
import codecs
import sys

print "Usage : python g_context_text.py <context.sgm> < <en.sgm> "
sys.stdin = codecs.getreader("utf-8")(sys.stdin)
context_f = codecs.open(sys.argv[1], "r", encoding="utf-8").readlines()

input_o = codecs.open("input.out", "w", encoding="utf-8")
context_o = codecs.open("context.out", "w", encoding="utf-8")
# parsing context
context = {}
for l in context_f:
    try:
        docid, sentid, sent = l.split("\t")
    except ValueError:
        continue
    #
    if docid not in context:
        context[docid] = [sent]
    else:
        context[docid].append(sent)
# print len(context["111"]) # ->614

top = 5
for l in sys.stdin:
    docid, sentid, sent = l.split("\t")
    try:
        sentid = int(sentid)
        # retrieve revious 5 context lines
        top5 = context[docid][sentid - top - 1: sentid - 1]
    except ValueError:
        print sentid
        top5 = []
    top5 = [l.strip() for l in top5]
    context_o.write(" ".join(top5) + '\n')
    input_o.write(sent)
