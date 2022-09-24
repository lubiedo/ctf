#!/usr/bin/env python3

i2c = open('untitled.txt', 'r').read().split('\n')[:-1]
cmds = []
for d in i2c:
    cmds.append(int(d[d.rindex(')')-4:d.rindex(')')],16))

def unsend(p1: int, p2: int, mode: int = 1):
    final  = (p1^1)&0xf0
    final += (p2^1)>>4
    return final

for cmd in range(0,len(cmds) -1, 6):
                # 1 write,      2 pulse,        3 pulse
    highbits = [cmds[cmd],      cmds[cmd+1],    cmds[cmd+2]]
    lowbits  = [cmds[cmd+3],    cmds[cmd+4],    cmds[cmd+5]]
    
    content = (highbits[0], lowbits[0])
    c = chr(unsend(content[0], content[1]))

    if c >= ' ' and c <= '~':
        print(c, end='')
