import sys
from urllib3 import encode_multipart_formdata
import requests

# https://tmx-api.newtranx.com/v1/las/3508/imports
url = "http://192.168.0.210:31954/v1/las/%s/imports" % sys.argv[2]

corpus = open(sys.argv[1], 'r').readlines()

p = 0
step = 100000
print ("Corpus size:%d" % len(corpus))
for i in range(0, len(corpus), step):
  lines = corpus[i:i + step]
  tmp = open('tmp.txt', 'w')
  for l in lines:
    tmp.write(l)
  
  DATA = {"data": ('tmp.txt', open('tmp.txt', 'rb').read(), 'text/plain')}
  DATA = encode_multipart_formdata(DATA)
  # print(DATA)
  response = requests.post(url, data=DATA[0], headers={'Content-Type': DATA[1], 'Authorization': 'bearer eyJraWQiOiJrMSIsInR5cCI6IkpXVCIsImFsZyI6IlJTMjU2In0.eyJleHAiOjE1NzQ0ODk3NzgsInVzZXJpZCI6ImM3MGUzYzAzMjI0NTQ3ZGU4ZGE5NWY2NjViMGQ4YjMyIiwidGlkIjoxODIzMywiY2xpZW50X2lkIjoiNmFjODdkOWJhZDhiNDcyZGFmNTBiZmY2MmUwNmEzY2UiLCJqdGkiOiJmZDc4Y2FjMmIyMWM0ZTdmYmM2NTYxNzRmNzQ1NmYxNiJ9.iNPQKbBBEiOXHC6P-kGDjAU7JFFjOCeNJkyjirfM7-wfm00pFdmZWHHAKHmPaBF0xPbiaBTJiaF2V9afsL34w3JRahDcmNXNQ4NPNAd5fOsqEmMZmYHUcA5rFmNMW5nE_WQl7QdPVcHgAgaNfOIY_F9ETYxeLBGWn-3vPt4-dcS6FymlK1YjM6avAl8YCEtcR7tk-iz_r90mUsWKTNnZV_8XIOC2oKm3DwPe3d9bqjJm6N_QDPVZf8IEsFDLD37MI3QGgb31YiPLHI6SkIRI4nKeTWlqQOHgHe87Fl67DECxsyUqC5ytlyw4GXgmnjEzghTP5JnzhrKI2ZFtrGeCVA'})
  print(response.content.decode())
  print("Page:%d" % i)