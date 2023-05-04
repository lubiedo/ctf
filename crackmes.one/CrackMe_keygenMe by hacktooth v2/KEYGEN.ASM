; https://crackmes.one/crackme/642189db33c5d447bc761e29
; cedric
format PE GUI 4.0
entry start

include 'win32a.inc'

USER_ID = 101
KEY_ID  = 102

macro mod [n]
{
      push eax ecx
      mov ecx,n
      cdq
      idiv ecx
      pop eax ecx
}

section '.text' code readable executable
        start:
                invoke GetModuleHandle,0
                invoke DialogBoxParam,eax,1,HWND_DESKTOP,DialogProc,0
                invoke ExitProcess, 0

proc DialogProc hwnd,umsg,wparam,lparam
     cmp [umsg],WM_CLOSE
     je .wm_close
     cmp [umsg],WM_INITDIALOG
     je .wm_init
     cmp [umsg],WM_COMMAND
     je .wm_cmd
     xor eax,eax
     jmp .return
.wm_cmd:
     mov edx,[wparam]
     cmp dx, USER_ID
     jne .done
     shr edx,16
     cmp edx,EN_CHANGE
     jne .done
     invoke GetDlgItemText,[hwnd],USER_ID,key,128
     mov esi,key
     call generate_key
     invoke SetDlgItemText,[hwnd],KEY_ID,key
     jmp .done
.wm_init:
     jmp .done
.wm_close:
     invoke EndDialog,[hwnd],0
.done:
     mov eax,1
.return:
     ret
endp

generate_key:
        call len
        mov [size],eax
        cld
        xor ecx,ecx
.repeat:
        lodsb
        or al,al
        jz .finish
        push ecx
        sub eax,[size]
        sub eax,ecx

        cmp al,'0'
        jge @f
        mul ecx
        mod 10
        mov eax,edx
        add eax,'0'
        jmp .save_char
     @@:
        cmp al,'9'
        jle @f
        cmp al,'A'
        jge @f
        mod 26
        mov eax,edx
        add eax,'A'
        jmp .save_char
     @@:
        cmp al,'Z'
        jle @f
        cmp al,'a'
        jge @f
        mod 26
        mov eax,edx
        add eax,'a'
        jmp .save_char
     @@:
        cmp al,'z'
        jl .save_char

        mod 26
        mov eax,'z'
        sub eax,edx
.save_char:
        pop ecx
        mov [key+ecx],al
        inc ecx
        jmp .repeat
.finish:
        ret

len:
        push esi
        xor ecx,ecx
     @@:
        lodsb
        or al,0
        jz @f
        inc ecx
        jmp @b
     @@:
        pop esi
        mov eax,ecx
        ret


section '.bss' readable writable
        size   dd 0
        key    rb 128

section '.idata' import data readable writable
        library kernel32,'KERNEL32.DLL',\
                user32,'USER32.DLL'

        import kernel32,\
               ExitProcess,'ExitProcess',\
               GetModuleHandle,'GetModuleHandleA'

        import user32,\
               DialogBoxParam,'DialogBoxParamA',\
               GetDlgItemText,'GetDlgItemTextA',\
               SetDlgItemText,'SetDlgItemTextA',\
               EndDialog,'EndDialog'

section '.rsrc' resource data readable
        directory RT_DIALOG,dialogs

        resource dialogs,\
                 1,LANG_ENGLISH+SUBLANG_DEFAULT,keygen

        dialog keygen,'Keygen',100,100,160,45,WS_CAPTION+WS_POPUP+WS_SYSMENU+DS_MODALFRAME
               dialogitem 'STATIC','&User:',-1,10,10,20,10,WS_VISIBLE
               dialogitem 'EDIT','',USER_ID,30,10,120,10,WS_VISIBLE+WS_BORDER+WS_TABSTOP
               dialogitem 'STATIC',' Key:',-1,10,25,30,10,WS_VISIBLE
               dialogitem 'EDIT','',KEY_ID,30,25,120,10,WS_VISIBLE+WS_BORDER+WS_TABSTOP
        enddialog
