#!/usr/bin/env python3

data = None
with open('./msg.enc', 'r') as fd:
    data = fd.read()

import binascii
data = binascii.unhexlify(data)

def compare(s: int) -> str:
    for c in range(0xff):
        if ((123*c+18)&0xff) == s:
            return chr(c)
    return None

for b in data:
    print(compare(b), end='')
