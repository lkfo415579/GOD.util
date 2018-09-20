# -*- encoding=utf8 -*-
import codecs
import sys
from tqdm import tqdm
import multiprocessing

s_lines = codecs.open(sys.argv[1], 'r').readlines()
t_lines = codecs.open(sys.argv[2], 'r').readlines()
# muti process
totoal_cpu = multiprocessing.cpu_count() - 2
# found one side matched lines


def find_matches(source, i):
    source_matched = []
    pbar = tqdm(total=len(source))
    for l1 in source:
        # display pbar
        if i % 1000 == 0:
            pbar.update(1000)
        j = i + 1
        for l2 in s_lines[j:]:
            if l1 == l2:
                source_matched.append((i, j))
                # print "matched[%d-%d]" % (i, j)
            j += 1
        i += 1
    return source_matched


def run_find_matches(args):
    return find_matches(args[0], args[1])


def set_up(source):
    privot = len(source) / totoal_cpu
    source_list = [None] * totoal_cpu
    index_list = []
    for cpu_id in range(0, totoal_cpu - 1):
        source_list[cpu_id] = source[cpu_id * privot:(cpu_id + 1) * privot]
        index_list.append(cpu_id * privot)
    source_list[-1] = source[(totoal_cpu - 1) * privot:]
    index_list.append((totoal_cpu - 1) * privot)
    return source_list, index_list


def run_main_find_match(lines):
    source_list, index_list = set_up(lines)
    print index_list
    s_matched = []
    p = multiprocessing.Pool(processes=totoal_cpu)
    sets = []
    for i, tmp in enumerate(source_list):
        sets.append((tmp, index_list[i]))
    s_matched = p.map(run_find_matches, sets)
    p.close()
    return s_matched


# find matches
s_matched = run_main_find_match(s_lines)
t_matched = run_main_find_match(t_lines)

# both matches lines
both = []
for i, match in enumerate(s_matched):
    for j, match_j in enumerate(t_matched):
        if match == match_j:
            # both match
            both.append(match[0])
        else:
            if match[0] > match_j[0]:
                break
# output two no duplicate corpus
print both[:5]
print "Outputing final corpus"
s_output = codecs.open(sys.argv[1] + ".nodup", 'wa')
t_output = codecs.open(sys.argv[1] + ".nodup", 'wa')
pbar = tqdm(total=len(s_lines))
for i, l in enumerate(s_lines):
    if i % 1000 == 0:
        pbar.update(1000)
    if not (i in both):
        s_output.write(l)
        t_output.write(t_lines[i])
