# -*- encoding=utf8 -*-
import codecs
import sys
from tqdm import tqdm

s_lines = codecs.open(sys.argv[1], 'r', encoding='utf8').readlines()
t_lines = codecs.open(sys.argv[2], 'r', encoding='utf8').readlines()


s_big_map = {}


def create_big_map(lines):
    big_map = {}
    for i, l in enumerate(lines):
        length = len(l)
        try:
            big_map[length].append((l, i))
        except KeyError:
            big_map[length] = [l]
    return big_map


def find_match(big_map, lines):
    matched = []
    for index, l in enumerate(tqdm(lines)):
        length = len(l)
        for tmp_tuple in big_map[length]:
            # (sent, index)
            if tmp_tuple[0] == l:
                # match bitch
                matched.append((index, tmp_tuple[1]))
    return matched


s_big_map = create_big_map(s_lines)
t_big_map = create_big_map(t_lines)

print "S_MATCH..."
s_match = find_match(s_big_map, s_lines)
print "T_MATCH..."
t_match = find_match(t_big_map, t_lines)

# both matches lines
both = []
record = []
for i, match in enumerate(s_match):
    for j, match_j in enumerate(t_match):
        if match == match_j:
            # both match
            record.append((match[0], match[1]))
            both.append(match[0])
        else:
            if match[0] > match_j[0]:
                break
# output two no duplicate corpus
print record[:5]
print "Outputing final corpus"
s_output = codecs.open(sys.argv[1] + ".nodup", 'wa', encoding='utf8')
t_output = codecs.open(sys.argv[2] + ".nodup", 'wa', encoding='utf8')
# record
record_f = codecs.open("tmp.record", 'wa', encoding='utf8')
for tmp in record:
    record_f.write(str(tmp) + "\n")
record_f.close()
#
pbar = tqdm(total=len(s_lines))
for i, l in enumerate(s_lines):
    if i % 1000 == 0:
        pbar.update(1000)
    if not (i in both):
        s_output.write(l)
        t_output.write(t_lines[i])

print ("DONE")
