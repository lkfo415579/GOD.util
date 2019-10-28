# -*- encoding=utf-8 -*-
import codecs
import sys
from regex import Regex

input = codecs.open(sys.argv[1], 'r', encoding='utf-8')

end_symbols = ["。", "？"]
quotes_symbols = ["“", "”"]
hyps_re = Regex(r'^[—>]+')

num = 0
for line in input:
    line = line.strip()
    # too damn short
    if len(line) < 3:
        continue
    # quotes are not match
    last_quote_count = line.count(quotes_symbols[1])
    if line.count(quotes_symbols[0]) != last_quote_count and line[0] != quotes_symbols[0]:
        continue
    if line[0] == quotes_symbols[0] and last_quote_count == 0:
        line = line[1:]
    # first hyps
    line = hyps_re.sub('', line)
    # replcae by hard code term
    line = line.replace("(来源: )", "")
    # final strip
    line = line.strip()
    print(line)
    num += 1

