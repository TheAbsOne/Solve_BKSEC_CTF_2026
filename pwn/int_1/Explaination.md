# CTF Write-up: int_1 (Integer Overflow)

**Date:** 2026-02-17
**Author:** Phạm Thịnh (HUST - IT-E15)
**Category:** Pwn / Logic
**Technique:** Signed Integer Overflow

---

## 1. Challenge Analysis
**Đề bài:**
Chương trình yêu cầu nhập 2 số nguyên dương (`v4`, `v5`). Sau đó tính tổng `v6 = v4 + v5`.
- Điều kiện đầu vào: `v4 >= 0` và `v5 >= 0`.
- Điều kiện chiến thắng (Win Condition): Nếu tổng `v6 < 0`, chương trình sẽ chạy `system("/bin/sh")`.

**Checksec:**
- **Canary:** Bật (Enabled) - *Nhưng không quan trọng vì không khai thác lỗi bộ nhớ.*
- **PIE:** Bật (Enabled) - *Không quan trọng vì không cần địa chỉ bộ nhớ.*
- **NX:** Bật (Enabled).

**Nghịch lý:**
Làm thế nào để **Dương + Dương = Âm**?

---

## 2. Vulnerability (Lỗ hổng)
Lỗ hổng nằm ở giới hạn lưu trữ của kiểu dữ liệu **Signed 32-bit Integer**.

### Cơ chế gốc rễ (Root Cause):
- Máy tính sử dụng quy tắc **Bù 2 (Two's Complement)** để lưu số âm.
- Bit đầu tiên (MSB) là bit dấu: `0` là Dương, `1` là Âm.
- Giới hạn của số dương (`int`): `0x7FFFFFFF` = **2,147,483,647**.
- Khi ta cộng thêm 1 vào số lớn nhất này:
  `0x7FFFFFFF + 0x00000001 = 0x80000000`
- Trong hệ Bù 2, `0x80000000` được hiểu là số âm nhỏ nhất: **-2,147,483,648**.

=> Hiện tượng này gọi là **Integer Overflow** (Tràn số nguyên).

---

## 3. Exploitation Strategy (Chiến thuật)
Để thỏa mãn điều kiện `v6 < 0`, ta cần làm tràn biến tổng `v6`.

**Payload:**
- **Input 1:** `2147483647` (Giá trị lớn nhất của số dương - INT_MAX).
- **Input 2:** `1` (Số dương nhỏ nhất).

**Kết quả:**
- Logic toán học: `2147483647 + 1 = 2147483648`.
- Logic máy tính: `0x7FFFFFFF + 0x1 = 0x80000000` -> **-2147483648** (Số Âm).
- Điều kiện `if (v6 < 0)` trả về TRUE -> **Lấy được Shell**.

---

