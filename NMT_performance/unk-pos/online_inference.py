# -*- encoding=utf-8 -*-
import codecs
import sys
import requests

IP = "192.168.50.15"
# PORT = 2014
PORT = 2076
sys.stdin = codecs.getreader("UTF-8")(sys.stdin)
sys.stdout = codecs.getwriter("UTF-8")(sys.stdout)

for line in sys.stdin:
    line = line.strip()
    if line == '</s>':
        continue
    r = requests.post("http://%s:%d/translate" % (IP, PORT), data={'text': line}, timeout=300)
    r = r.json()
    trans_word = r['translation'][0]['translated'][0]['text']
    sys.stdout.write(line + " " + trans_word + '\n')
