[BITS 64]

section .data
    index dq 24
    data  dq 16

section .text
    global _start
    global _overwrite
    global _dll
    global _exit

_start:
    mov rax, 1
    mov rcx, 1
    call _overwrite

_overwrite:
    mov rax, 0
    mov rcx, 0
    call _dll

_dll:
    mov rax, [rel index]   ; RIP-relative safe access
    mov rcx, [rel data]    ; RIP-relative safe access
    ret

_exit:
    mov rax, 60            ; syscall: exit
    xor rdi, rdi           ; exit code 0
    syscall

    