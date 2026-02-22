# Custom Format String Payload

## Overview
This exploit utilizes a **custom-crafted payload** instead of the standard `pwntools.fmtstr_payload` function. 

## Rationale
The decision to manually construct the payload was driven by the strict **32-byte (0x20) input limitation** of the `fgets()` function. 
* Standard automated tools often generate payloads exceeding this limit due to over-alignment and byte-by-byte writing (`%hhn`).
* Our manual approach optimizes the payload length to exactly 24 bytes by using **partial overwrites** (`%hn`) and precise stack alignment.

## Further Reading
For a detailed breakdown of the manual calculation and alignment logic, please refer to: 
`fmt_1/Explanation.md`