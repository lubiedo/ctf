#/usr/bin/env python3

from unicorn import *
from unicorn.x86_const import *

import numpy as np
import random
from pwn import *
from binascii import unhexlify

context.log_level='warn'

keydata = '/kfgvhUrZAjI+RIGqXTssE0+9QULEanJ1NPsduZD3GHWhKpCUOAnPlCAJ8k7c32S6ckUKiXMS8x9+KLY7bubYgvQ+AIxNk682mnxKSDBl3pa2wKgZTvD2SJCVexS2dPGC9bLGPT/avHPR8F52y8nsQDp64tPoQ7fb9uNIvJy+NpThnqxwVlFLmE5SKABh5BeCl6kLpqbNNTsQ6U8Zm4Ac+qX1xJbLr4kqGZE+me+dUqKeSZPlMRelhAPQe/w1PApIa+uGZUL+kVXShBASPtIYDU8EtAdVvZ/ao3ITl/JgYqJoyyMrcwfEhFxSm25RCjUs9MJqJtWeRRRl4c7ivQSDg=='

def genkey(l: int):
    out = [0]*(l*2)
    for i in range(0, 255):
        out[i+2] = i

    buf = list(keydata)
    j = 0
    dest = out[2:]
    for i in range(0,255):
        # 0000178c  mov     eax, dword [rbp-0x120 {counter2}]
        # 00001792  movsxd  rdx, eax
        # 00001795  mov     rax, qword [rbp-0x118 {dest_1}]
        # 0000179c  add     rax, rdx
        # 0000179f  movzx   eax, byte [rax]
        # 000017a2  movzx   edx, al
        # 000017a5  mov     eax, dword [rbp-0x11c {j}]
        # 000017ab  add     edx, eax
        # 000017ad  mov     eax, dword [rbp-0x120 {counter2}]
        # 000017b3  cdqe
        # 000017b5  movzx   eax, byte [rbp+rax-0x110 {buf}]
        # 000017bd  movzx   eax, al
        # 000017c0  add     eax, edx
        # 000017c2  cdq
        # 000017c3  shr     edx, 0x18
        # 000017c6  add     eax, edx
        # 000017c8  movzx   eax, al
        # 000017cb  sub     eax, edx
        # 000017cd  mov     dword [rbp-0x11c {j}], eax
        c = dest[i]
        c += j
        d = ord(buf[i])
        d += c
        c = c >> 0x18
        d += c
        d = d & 0xff
        d -= c
        j = d

        # 000017d3  mov     eax, dword [rbp-0x11c {j}]
        # 000017d9  movsxd  rdx, eax
        # 000017dc  mov     rax, qword [rbp-0x118 {dest_1}]
        # 000017e3  add     rdx, rax
        # 000017e6  mov     eax, dword [rbp-0x120 {counter2}]
        # 000017ec  movsxd  rcx, eax
        # 000017ef  mov     rax, qword [rbp-0x118 {dest_1}]
        # 000017f6  add     rax, rcx
        # 000017f9  mov     rsi, rdx
        # 000017fc  mov     rdi, rax
        # 000017ff  call    swap
        # 00001804  add     dword [rbp-0x120 {counter2}], 0x1
        dest[i], dest[j] = dest[j], dest[i]
    out[2:] = dest
    return out

# def _mutate(m: bytes):
#     r  = b'MmM2ZTk5NDQ0NzBiNjQ5MjY1NWNkMTFkNGYyYjNhYzU0MD0df82e5bEC71o='
#     rl = len(r) - 0xc
#     out = [b'', b'', b'', b'']
#     c = m
#     for j in reversed(list(range(0,3))):
#         if c == 0:
#             break
#         out[j] = r[c % 0xA + rl].to_bytes(1)
#         c = c//0xA
#     out[3] = b':'
#     return out

def scramble(m):
    global key
    BASE = 0x400000
    STACK_ADDR = 0x0
    STACK_SIZE = 1024*1024

    mu = Uc (UC_ARCH_X86, UC_MODE_64)
    mu.mem_map(BASE, STACK_SIZE)
    mu.mem_map(STACK_ADDR, STACK_SIZE)

    mu.mem_write(BASE, read("./door-code"))
    mu.reg_write(UC_X86_REG_RSP, STACK_ADDR + STACK_SIZE - 1)

    buff_addr = STACK_ADDR + (STACK_SIZE // 2)

    mu.reg_write(UC_X86_REG_RDI, buff_addr)
    mu.mem_write(buff_addr, key)
    mu.reg_write(UC_X86_REG_ESI, m)
    def hook_code(mu, address, size, user_data):
        # print('>>> Tracing instruction at 0x%x, instruction size = 0x%x' %(address, size))
        return

    mu.hook_add(UC_HOOK_CODE, hook_code)
    mu.emu_start(0x401851, 0x401938)

    key = bytes(mu.mem_read(buff_addr, 256))
    return mu.reg_read(UC_X86_REG_RAX)

    # key[1] += key[key[0] + 2]
    # key[0] += 1
    # key[key[0] + 2], key[key[1] + 2] = key[key[1] + 2] & 0xFF, key[key[0] + 2] & 0xFF
    # return key[((key[key[0] + 2] + key[key[1] + 2]) & 0xFF) + 2] ^ m

def mutate(m: bytes):
    r  = b'MmM2ZTk5NDQ0NzBiNjQ5MjY1NWNkMTFkNGYyYjNhYzU0MD0df82e5bEC71o='
    rl = len(r) - 0xc
    out = [b'', b'', b'', b'']
    c = m
    for j in reversed(list(range(0,3))):
        if c == 0:
            break

        # 00001383  movzx   edx, cl
        # 00001386  mov     eax, edx
        # 00001388  shl     eax, 0x2
        # 0000138b  add     eax, edx
        # 0000138d  shl     eax, 0x3
        # 00001390  add     eax, edx
        # 00001392  lea     edx, [rax*4]
        # 00001399  add     eax, edx
        # 0000139b  shr     ax, 0x8
        # 0000139f  mov     edx, eax
        # 000013a1  shr     dl, 0x3
        # 000013a4  mov     eax, edx
        # 000013a6  shl     eax, 0x2
        # 000013a9  add     eax, edx
        # 000013ab  add     eax, eax
        # 000013ad  sub     ecx, eax
        # 000013af  mov     edx, ecx
        # 000013b1  movzx   edx, dl
        cc = c
        n = cc
        n <<= 2
        n += cc
        n <<= 3
        n += cc
        cc = n * 4
        n += cc & 0xFFFFFFFF
        n = (n & 0xFFFF0000) | ((n & 0xFFFF)>>8)
        cc = n
        cc = ( cc & 0xFFFFFF00) | ((cc & 0xFF)>>3)
        n = cc
        n <<= 2
        n += cc
        n += n
        cc = (c - n) & 0xFF

        # 000013b4  mov     eax, dword [rbp-0x4 {len}]
        # 000013b7  lea     ecx, [rdx+rax]
        pos = (rl + cc)&0xFFFFFFFF

        out[j] = r[pos].to_bytes(1)

        # 000013df  movzx   edx, al
        # 000013e2  mov     eax, edx
        # 000013e4  shl     eax, 0x2
        # 000013e7  add     eax, edx
        # 000013e9  shl     eax, 0x3
        # 000013ec  add     eax, edx
        # 000013ee  lea     edx, [rax*4]
        # 000013f5  add     eax, edx
        # 000013f7  shr     ax, 0x8
        # 000013fb  shr     al, 0x3
        cc = c
        n = cc
        n <<= 2
        n += cc
        n <<= 3
        n += cc
        cc = n * 4
        n += cc & 0xFFFFFFFF
        n = (n & 0xFFFF0000) | ((n & 0xFFFF)>>8)
        n = (n & 0xFFFFFF00) | ((n & 0xFF)>>3)

        c = n & 0xFF
    out[3] = b':'
    return out

# extracted
# key = [0, 0, 47, 142, 3, 108, 230, 83, 103, 96, 137, 247, 71, 1, 210, 233, 134, 50, 158, 199, 113, 7, 164, 73, 219, 107, 110, 242, 69, 80, 222, 135, 180, 124, 205, 60, 38, 68, 204, 85, 65, 163, 140, 252, 24, 240, 99, 190, 126, 100, 70, 97, 28, 77, 231, 213, 223, 11, 109, 185, 94, 61, 67, 175, 87, 159, 143, 196, 37, 254, 2, 31, 162, 211, 148, 64, 215, 91, 12, 129, 236, 56, 6, 114, 248, 45, 192, 101, 156, 179, 36, 246, 166, 146, 245, 66, 178, 44, 39, 53, 63, 128, 193, 74, 189, 174, 234, 118, 176, 167, 20, 105, 121, 25, 17, 243, 151, 177, 217, 186, 72, 187, 214, 9, 19, 147, 228, 122, 119, 237, 123, 112, 86, 54, 79, 52, 136, 224, 195, 57, 171, 170, 218, 58, 155, 160, 35, 161, 88, 203, 139, 226, 255, 104, 149, 81, 184, 188, 42, 169, 172, 181, 183, 82, 78, 18, 59, 212, 34, 5, 207, 221, 238, 30, 95, 138, 154, 225, 249, 120, 33, 116, 76, 165, 16, 125, 253, 4, 197, 51, 198, 141, 93, 206, 0, 23, 208, 239, 8, 115, 232, 200, 106, 144, 111, 227, 168, 157, 98, 55, 89, 244, 182, 173, 202, 241, 75, 102, 131, 49, 43, 127, 153, 46, 90, 48, 201, 32, 235, 251, 10, 250, 27, 209, 92, 62, 22, 145, 26, 40, 117, 130, 229, 14, 216, 84, 133, 152, 220, 15, 21, 13, 191, 132, 150, 194, 41, 29, 0, 0, 0, 0, 0, 0]
# or generated
key = genkey(256)
key = b''.join(list(map(lambda l: l.to_bytes(1), key)))

mutated = []
for i in range(0, 256):
    mutated.append(b''.join(mutate(i)).decode())
    print(f'{i} = {mutated[i]}')

scrambled = []
for i in range(0, 8):
    scrambled.append(scramble(i) ^ i)
print(f'{scrambled = }')

con = remote('localhost', 6666)
con.recv()
prompt = con.recv()
log.warn(f'Door {prompt}')

prompt = prompt.split(b':')[:-1]

final = [0]*8
for i in range(len(prompt)):
    piece = prompt[i].decode()
    m = mutated.index(piece + ':')
    final[i] = m ^ scrambled[i]

final = int.from_bytes(bytes(final), 'little') ^ 0x0503050506
final = f'{final:x}'.encode()
print(final)
con.sendline(final)
print(con.recv())
con.close()
