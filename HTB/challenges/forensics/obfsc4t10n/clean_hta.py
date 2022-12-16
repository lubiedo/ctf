#!/usr/bin/env python3

import sys
import re

file = sys.argv[1]
data = ''
with open(file, 'r') as fd:
    data = fd.read()

data = re.sub(r'(?:"")*\&(?:"")*', '', data)
pos = data.index('Chr(')
while pos > 0:
    closing = data.index(')', pos)
    charcode = data[pos+4:closing]
    data = data.replace(f'Chr({charcode})', chr(int(charcode)))

    if pos+5 > len(data):
        break
    pos = data.find('Chr(', pos+5)
print(data)
