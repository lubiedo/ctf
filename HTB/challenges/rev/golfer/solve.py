#!/usr/bin/env python3

from capstone import *

offsets = []

code = b''
with open('golfer', 'rb') as fd:
    code = fd.read()

md = Cs(CS_ARCH_X86, CS_MODE_32)
md.detail = True

for op in md.disasm(code[0x4c:], 0x0):
    if op.mnemonic != 'mov':
        continue
    if not op.op_str.startswith('ecx'):
        continue
    off = op.op_str.split(', ')
    off = int(off[1], 16) & 0xff
    offsets.append(off)

print(''.join([chr(code[off]) for off in offsets]))
