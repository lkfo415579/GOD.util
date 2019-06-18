# -*- coding: utf-8 -*-
from pyvi import ViTokenizer

import codecs
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

sys.stdin = codecs.getreader('UTF-8')(sys.stdin)
sys.stdout = codecs.getwriter('UTF-8')(sys.stdout)

for line in sys.stdin:
    line = line.strip()
    line = ViTokenizer.tokenize(line).decode('utf-8').strip()
    sys.stdout.write(line + "\n")
