RET  = 0xC3 
buff = [
    0x50,
    0x5E,
    0x5E,
    0xA3,
    0x4F,
    0x5B,
    0x51,
    0x5E,
    0x5E,
    0x97,
    0xA3,
    0x80,
    0x90,
    0xA3,
    0x80,
    0x90,
    0xA3,
    0x80,
    0x90,
    0xA3,
    0x80,
    0x90,
    0xA3,
    0x80,
    0x90,
    0xA3,
    0x80,
    0x90,
    0xA3,
    0x80,
    0x90,
    0xA2,
    0xA3,
    0x6B,
    0x7F
]


for i in buff:
    print(hex(RET-i)[2:], end='')
print('')
