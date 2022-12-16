#!/usr/bin/env python3

import sys
import json
import re
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad,pad
from base64 import b64decode

CD ='Content-Disposition: form-data; ' 
IV = bytes([
    105,
    110,
    102,
    105,
    110,
    105,
    116,
    121,
    95,
    101,
    100,
    103,
    101,
    104,
    116,
    98])
KEY = b'\x4d\x65\xbd\xba\xd1\x83\xf0\x02\x03\xb1\xe8\x0c\xf9\x6f\xba\x54\x96\x63\xda\xbe\xab\x12\xfa\xb1\x53\xa9\x21\xb3\x46\x97\x5c\xdd'


def isb64(s):
    return (re.match(r'^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{2}==)?$', s) != None)

def decrypt(s):
    c = AES.new(KEY, AES.MODE_CBC, iv=IV)
    return c.decrypt(pad(s, 16))


file = sys.argv[1]
data = json.loads(open(file, 'r').read())

for http in data['data']:
    i, r = http
    if not isinstance(r, str):
        continue
    
    print(f'{i}#{"="*20}')
    form = r.find(CD)
    if form > 0:
        tmp = r[form + len(CD):]
        r = tmp[tmp.index('\r\n\r\n')+4:tmp.rindex('\r\n--')]
    
    if not isb64(r):
        print(r)
        continue
    
    print(decrypt(b64decode(r)).decode('latin1'))

