# -*- coding: utf-8 -*-
import sys
import codecs
from polyglot.text import Text
load = "We are good"
Text(load)
print ("Loaded POS model")


def main():
    Eng_side = 1
    source_data = codecs.open(sys.argv[1], 'r', encoding='utf-8').readlines()
    target_data = codecs.open(sys.argv[2], 'r', encoding='utf-8').readlines()
    #
    align = []
    for index, sent in enumerate(target_data):
        target_data[index], tmp = sent.split(" ||| ")
        #
        tmp = tmp.split()
        tmp = [int(a.split("-")[1]) for a in tmp]
        align.append(tmp)
    print ("S:", source_data[:5])
    print ("T:", target_data[:5])
    print (align[:5])
    if Eng_side == 0:
        for sent in source_data:
            text = Text(sent)
            print (text.pos_tags)
            sys.exit()
    else:
        for sent in target_data:
            text = Text(sent)
            Noun_index = []
            index = 0
            for word, POS in text.pos_tags:
                if POS == "NOUN":
                    Noun_index.append(index)
                index += 1
            print (Noun_index)

            sys.exit()


if __name__ == '__main__':
    # sys.stdin = codecs.getreader('utf-8')(sys.stdin)
    # sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
    main()
