import sys

if len(sys.argv) != 2:
    quit(1)

file  = sys.argv[1]

needs = [
    '0x0000:MZ',
    '0x00FC:\x64\x86',
    '0x0100:THIS',
]

c = bytearray(open(file, 'rb').read())

for need in needs:
    (addr, data) = need.split(':')
    addr = int(addr, 16)
    for i in range(len(data)):
        c[addr+i] = ord(data[i])
with open(file, 'wb') as fd:
    fd.write(bytes(c))
