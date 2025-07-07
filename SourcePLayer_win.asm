[BITS 64]

section .data
    index dq 24
    data dq 16

section .text
    global _start
    global _overwrite
    global _dll

_start:
    mov rax,1
    mov rcx,1
    
    call _overwrite

_overwrite:
    mov rax,0
    mov rcx,0
    call _dll

_dll:
    mov rax,[index]
    mov rcx,[data]




