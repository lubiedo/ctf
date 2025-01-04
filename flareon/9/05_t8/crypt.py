#!/usr/bin/env python3

from base64 import b64decode, b64encode
from hashlib import md5

unicode = lambda s: s.encode('utf-16-le')


class RC4():
    S = []
    key = None

    def __init__(self, key):
        j = 0
        S = [i for i in range(256)]
        
        # KSA Phase
        for i in range(256):
            j = (j + S[i] + ( key[i % len(key)] )) % 256
            S[i] , S[j] = S[j] , S[i]

        self.S = S
        self.key = key
        return 
    
    def encrypt(self, data):
        out = []
        S = self.S

        # PRGA Phase
        i = j = 0
        for char in data:
            i = ( i + 1 ) % 256
            j = ( j + S[i] ) % 256
            S[i] , S[j] = S[j] , S[i]
            out.append(char ^ S[(S[i] + S[j]) % 256])
        return bytes(out) 

import sys

string = unicode('srpf8Su2Ev4=')
string_http = 'TdQdBRa1nxGU06dbB27E7SQ7TJ2+cd7zstLXRQcLbmh2nTvDm1p5IfT/Cu0JxShk6tHQBRWwPlo9zA1dISfslkLgGDs41WK12ibWIflqLE4Yq3OYIEnLNjwVHrjL2U4Lu3ms+HQc4nfMWXPgcOHb4fhokk93/AJd5GTuC5z+4YsmgRh1Z90yinLBKB+fmGUyagT6gon/KHmJdvAOQ8nAnl8K/0XG+8zYQbZRwgY6tHvvpfyn9OXCyuct5/cOi8KWgALvVHQWafrp8qB/JtT+t5zmnezQlp3zPL4sj2CJfcUTK5copbZCyHexVD4jJN+LezJEtrDXP1DJNg=='

if len(sys.argv) >= 2:
    key = sys.argv[1]
    h = md5()
    if '@' in key:
        h.update(unicode(f'{key}'))
    else:
        h.update(unicode(f'FO9{key}'))

    digest = unicode(h.hexdigest())
    print(f'key:{key}, digest:{digest.decode()}')

    rc4 = RC4(digest)
    received = rc4.encrypt(b64decode(string))
    print(f'\treceived: {received.decode("latin1")}')
    
    rc4 = RC4(digest.decode('utf-16-le').encode('latin1'))
    sent = rc4.encrypt(b64decode(string_http))
    print(f'\tsent:{sent}')
else:
    emails = [unicode(f'{chr(letter)}@flare-on.com') for letter in range(97, 123)]
    emails.append(unicode(' @flare-on.com'))
    for email in emails:
        h = md5()
        h.update(email)

        digest = unicode(h.hexdigest())
        print(f'email:{email.decode()}, digest:{digest.decode()}')
        
        # encrypt
        rc4 = RC4(digest)
        result = rc4.encrypt(string)
        sent = b64encode(result)
        print(f'\tsent:{sent}')

        # decrypt
        received = rc4.encrypt(b64decode('GvgU3HiGF0w='))
        print(f'\treceived: {received}')

    
