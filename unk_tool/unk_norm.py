#!/usr/bin/python
# -*- coding: utf-8 -*-

import codecs
import sys
from regex import Regex

__UNK = Regex(r'(<unk>[\S\s]*?</unk>)')
sys.stdout = codecs.getwriter('UTF-8')(sys.stdout)
sys.stdin = codecs.getreader('UTF-8')(sys.stdin)

for line in sys.stdin:
    sys.stdout.write(__UNK.sub("<unk2>", line).strip() + "\n")
