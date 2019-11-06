# -*- coding: utf-8 -*-
# import codecs
import sys
from bs4 import BeautifulSoup
# sys.stdin = codecs.getreader('UTF-8')(sys.stdin)
# sys.stdout = codecs.getwriter('UTF-8')(sys.stdout)

for line in sys.stdin:
    line = line.strip()
    soup = BeautifulSoup(line, 'html.parser')
    print(soup.get_text())
    # sys.stdout.write(line + "\n")
