# -*- encoding=utf-8 -*-
import codecs
import sys
import requests
import json

# .py <port> < input > output

port = sys.argv[1]
sys.stdin = codecs.getwriter("UTF-8")(sys.stdin).readlines()
sys.stdout = codecs.getwriter("UTF-8")(sys.stdout)

for line in sys.stdin:
    r = requests.post('http://121.46.13.39:%s/translate' % port, data={'text': line})
    data = json.loads(r.text)
    data = data["translation"][0]["translated"]
    data = [ele["text"] for ele in data]
    tran = " ".join(data)
    sys.stdout.write(tran + "\n")
