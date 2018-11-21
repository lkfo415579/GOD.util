# -*- encoding=utf-8 -*-
import codecs
import sys


def consecutive_BPE(s, source, start):
    if s[-2:] == '@@':
        s = s[:-2] + consecutive_BPE(source[start + 1], source, start + 1)
    return s


# options
if len(sys.argv) > 4:
    use_lex_table = int(sys.argv[4])
else:
    use_lex_table = True

# python unk_replace.py nbest-unk.file source.file lex.file use_lex(1|0)
# marian new alignment version
sys.stdout = codecs.getwriter("UTF-8")(sys.stdout)
nbest_data = codecs.open(sys.argv[1], "r").readlines()
source_data = codecs.open(sys.argv[2], "r").readlines()
lex = codecs.open(sys.argv[3], "r").readlines()
# output unk tags temportalily
unk_tags_output = codecs.open("unk_tags", "w")
# read lex
LEX_TABLE = {}
for line in lex:
    s_term, t_term = line.split()[:2]
    if s_term not in LEX_TABLE:
        LEX_TABLE[s_term] = t_term
# main
for i_line, line in enumerate(nbest_data):
    target, align = line.split(" ||| ")
    # if source has no unk skip
    if target.find("<unk>") == -1:
        sys.stdout.write(target.decode('utf8') + '\n')
        pass
    else:
        # target to list
        target = target.strip()
        target = target.split()
        # POS replace unk procedure
        align = align.split()
        align_pos = {}
        for entity in align:
            # marian style
            # s, t = entity.split("-")
            # amun style
            t, s = entity.split("-")
            align_pos[int(t)] = int(s)
        # {target_pos: source_pos}, type : int
        source = source_data[i_line]
        source = source.strip()
        source = source.split()
        source.append("</s>")
        # replace unk tags
        all_unk_pos = [i for i, x in enumerate(target) if x == "<unk>"]
        for pos in all_unk_pos:
            # s is source_word
            s = source[align_pos[pos]]
            # contains @@
            s = consecutive_BPE(s, source, align_pos[pos])
            # inference
            t_term = "<unk>"
            if use_lex_table:
                try:
                    t_term = "#" + LEX_TABLE[s] + ":" + s + "#"
                except KeyError:
                    # Fucked there is no translation from dictionary
                    pass
            else:
                # use identity translation
                unk_tags_output.write(s + "\n")

            target[pos] = t_term
        sys.stdout.write(" ".join(target).decode('utf8') + "\n")
