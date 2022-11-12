#!/usr/bin/env python3

import re
import sys
from zlib import decompress
from base64 import b64decode


KEY = b'80e32263'

def main(args):
    indata = None
    if len(args) < 2:
        indata = input()
    else:
        indata = args[1]
    if not indata:
        return 1
    obfdata = re.findall(r'(?:0UlYyJHG87EJqEz6)*?6f8af44abea0(.+)351039f4a7b5', indata,  re.IGNORECASE)
    if len(obfdata) == 0:
        return 1
    print(b64decode(obfdata[0]))
    obfdata = b64decode(obfdata[0])
    data = ''
    i = 0
    for b in obfdata:
        data += chr(b ^ KEY[i % len(KEY)])
        i += 1
    print(decompress(data.encode('latin1')).decode())

if __name__ == "__main__":
    quit(main(sys.argv))
