#!/usr/bin/env python3

from capstone import *
from unicorn import *
from unicorn.x86_const import *

CODE = b'\x55\x8B\xEC\x83\xEC\x20\xEB\xFE\xE1\x60\xA1\x18\x93\x2E\x96\xAD\x73\xBB\x4A\x92\xDE\x18\x0A\xAA\x41\x74\xAD\xC0\x1D\x9F\x3F\x19\xFF\x2B\x02\xDB\xD1\xCD\x1A\x00\x3E\x39\x51\xFB\xA2\x11\xF7\xB9\x2C'
DISASM = dict()

def hook_code(uc, address, size, user_data):
    print("0x%08x:" % address, end='\t')
    tmp = uc.mem_read(address, size)
    for i in tmp:
        print("%02x" % i, end="")
    print(f'\t\t{DISASM[address]}')
    try:
        input()
    except:
        mu.emu_stop()

try:
    md = Cs(CS_ARCH_X86, CS_MODE_32 + CS_MODE_LITTLE_ENDIAN)
    ADDR = 0x1000

    for i in md.disasm(CODE, ADDR):
        DISASM[i.address] = i.mnemonic + ' ' + i.op_str

    mu = Uc(UC_ARCH_X86, UC_MODE_32)
    mu.mem_map(ADDR, 2*1024*1024)
    mu.mem_write(ADDR, CODE)
    mu.hook_add(UC_HOOK_CODE, hook_code)
    mu.reg_write(UC_X86_REG_ESP, ADDR * 2)
    mu.emu_start(ADDR, len(CODE))
except UcError as e:
    print(e)
