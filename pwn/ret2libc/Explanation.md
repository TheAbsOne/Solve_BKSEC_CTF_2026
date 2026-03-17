# 🎯 Write-up: Format String & Buffer Overflow Exploitation (Ret2Libc)

## 1. Protections Overview
Through binary analysis, the target executable is found to have the following security mechanisms enabled:
* **ASLR (Address Space Layout Randomization):** Enabled (Memory segments such as Stack, Heap, and Libc are randomized upon each execution).
* **NX (No-eXecute):** Enabled (Shellcode cannot be executed directly on the Stack).
* **RELRO (Relocation Read-Only):** Partial RELRO.


## 2. Exploitation Strategy
Given the presence of NX and ASLR, the exploitation strategy is divided into two phases:
1.  **Information Leak:** Leverage the **Format String** vulnerability to read data off the Stack, thereby leaking the return address (Saved RIP) of the C standard library (`libc.so.6`). This leak is used to calculate the **Libc Base Address**.
2.  **Code Reuse Attack:** Utilize **ROP (Return-Oriented Programming)**, specifically the **Ret2Libc** technique, to construct an execution chain that ultimately calls `system("/bin/sh")`. 
    * *Note: An additional `ret` ROP Gadget must be injected to bypass the Stack Alignment issue (ensuring the 16-byte boundary on x64 architecture), which prevents a Segmentation Fault when `glibc` executes the `movaps` instruction.*

---


## 3. Analysis and Exploitation Phase

### Phase I: Leaking the Libc Base Address

**1. Discovering the Format String Vulnerability (Fuzzing)**

Analyzing the execution flow reveals that the program prints user input via the `printf(s)` function without specifying a format string (Format specifier). 
Fuzz-File: fuzz.py
Fuzzing the input using the `fuzz.py` script with the `%<offset>$p` payload allows us to directly read pointers on the Stack. The fuzzing process reveals crucial leaked addresses:
* At offset *49*: A leaked address belonging to the `__libc_start_main` function.
* At offset *29*: A leaked address belonging to the `__libc_start_call_main` function.

**2. Offset Calculation (the distance from the libc base)**

Once a Stack address is leaked, we must pinpoint the exact instruction within `libc` it corresponds to in order to calculate the `Libc Base Address`.   
At the first look, relying on the GDB's resolved symbol can lead to a common exploitation pitfall. Consider the leaked address for `__libc_start_main`:  

``0x00007fffffffdcc8│+0x00d0: 0x00007ffff7c2a28b  →  <__libc_start_main+008b> mov r15, QWORD PTR [rip+0x1d8cf6]        # 0x7ffff7e02f88``  

It is tempting to naively extract the offset +008b in '<__libc_start_main+008b>'. However, this offset is strictly tied to the local execution environment. Since the remote server utilizes a different libc version (provided as *libc.so.6*), calculating the Libc Base Address using local GDB annotations will result in a payload failure.  
To determine the accurate offset, we must analyze the disassembly of `__libc_start_main` (or its underlying implementation `__libc_start_main_impl`). By executing the `telescope` command in GDB, we inspect the raw memory on the stack:  

``0x00007fffffffdcc8│+0x00d0: 0x00007ffff7c2a28b  →  <__libc_start_main+008b> mov r15, QWORD PTR [rip+0x1d8cf6]        # 0x7ffff7e02f88``  

This leaked value represents a **Saved RIP (Return Instruction Pointer)** stored on the stack. The critical question is: *Which function call pushed this specific return address?*   
Reviewing the disassembly, we observe multiple `call` instructions. By tracing the execution flow, we can rule out the calls that have already returned. The Saved RIP we leaked actually corresponds to the return address of the `__libc_start_call_main` invocation:   

``0x000055555557de3b <+123>:   call   0x55555557dd10 <__libc_start_call_main>``    
``0x000055555557de40 <+128>:   mov    r15,QWORD PTR [rip+0x1f0159]        # 0x55555576dfa0``  
``0x000055555557de47 <+135>:   mov    r14,QWORD PTR [r15]``    

The Saved RIP saves the address points to the next command -> The real offset we need to find is:   

``0x000055555557de40 <+128>:   mov    r15,QWORD PTR [rip+0x1f0159]        # 0x55555576dfa0``  

### Phase II: Exploiting - Take the flag

This is the easiest part, we ROPgadget the artifacts and lead the program to pop the shell

**Final product: Solve.py**

