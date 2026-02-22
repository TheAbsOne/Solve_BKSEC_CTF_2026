# 🚩 Writeup: Format String Vulnerability - Arbitrary Write (`fmt_1`)

## 🔍 1. Phân tích mục tiêu (Binary Analysis)
* File thực thi `fmt_1` là một binary 64-bit (amd64).
* Khi chạy, chương trình đưa ra một thông báo: "What do you want to say?".
* Nếu chúng ta nhập một chuỗi bình thường, chương trình sẽ in ra "You are not a hero." và kết thúc.
* Tuy nhiên, bằng cách phân tích tĩnh (Static Analysis) hoặc dịch ngược, ta phát hiện chương trình có gọi các hàm đáng chú ý như `printf`, `read`, `system` và chứa một biến toàn cục tên là `target`.
* Đặc biệt, chương trình có chứa chuỗi `/bin/sh`.

**Lỗ hổng gốc rễ (Root Cause):**
* Chương trình sử dụng hàm `printf(buf)` thay vì `printf("%s", buf)` để in dữ liệu người dùng nhập vào.
* Điều này gây ra lỗ hổng **Format String Vulnerability**, cho phép kẻ tấn công dùng các thẻ định dạng (như `%p`, `%x`) để rò rỉ bộ nhớ (Leak Memory) hoặc dùng thẻ `%n` để ghi đè dữ liệu tùy ý lên bộ nhớ (Arbitrary Write).

## 🎯 2. Kịch bản khai thác (Exploit Strategy)
* Mục tiêu tối thượng của bài này là ép chương trình gọi hàm `system("/bin/sh")` để lấy được shell.
* Để làm được điều đó, ta cần thỏa mãn điều kiện logic của chương trình: Biến `target` phải mang giá trị `0x6F726568` (chính là mã Hex của chuỗi `hero` ở dạng Little-Endian).

**Quy trình thực hiện:**
1. **Xác định địa chỉ của biến `target`:** Vì bài này không bật PIE (Position Independent Executable), biến toàn cục `target` sẽ nằm ở một địa chỉ bộ nhớ tĩnh trên phân vùng `.bss` hoặc `.data`. Ta có thể trích xuất trực tiếp bằng công cụ tĩnh.
2. **Tìm Offset của Buffer:** Bằng cách nhập chuỗi `AAAAAAAA.%p.%p.%p...` và quan sát vị trí xuất hiện của khối `0x4141414141414141`, ta xác định được mảng `buf` chứa input bắt đầu ở **offset thứ 10** trên Stack tính từ vị trí con trỏ của `printf`.
3. **Chế tạo Payload:** Xây dựng một chuỗi Format String phức tạp kết hợp giữa các thẻ `%c` (để bơm đủ số lượng ký tự cần thiết) và `%hhn` (để ghi từng byte vào địa chỉ `target`).

---

# 🧠 Deep Dive: Cơ chế hoạt động của `fmtstr_payload` & Thẻ định vị tham số

Là một sinh viên Bách Khoa đang theo đuổi Red Team, việc dùng tool như một "hộp đen" (blackbox) là điều tối kỵ. Tài liệu này mổ xẻ cơ chế gốc rễ bên dưới thư viện Pwntools và chuẩn POSIX C để hiểu chính xác từng byte được ghi vào bộ nhớ như thế nào.

---

## 🛠️ Phần 1: Phép thuật của `%[vị_trí]$[kiểu]` (Direct Parameter Access)

Trong ngôn ngữ C chuẩn, `printf` xử lý các tham số một cách tuần tự (trái sang phải). Tuy nhiên, chuẩn POSIX (áp dụng trên hệ điều hành Linux) cung cấp một tính năng mở rộng gọi là **Truy cập tham số trực tiếp (Positional Arguments)** bằng cách chèn thêm dấu `$` vào thẻ định dạng.

### 1. Ký tự `$` làm nhiệm vụ gì?
* Khi ta truyền `%10$p` vào `printf`, ta đang ra lệnh: *"Bỏ qua thứ tự đọc tuần tự. Hãy nhảy thẳng đến tham số thứ 10 (tính từ sau chuỗi format) và in nó ra dưới dạng con trỏ"*.

**Cơ chế dưới thanh ghi và RAM (Calling Convention):**
1. CPU nhận lệnh `%10$p`.
2. Theo quy ước x86_64, 5 thanh ghi đầu tiên (`RSI, RDX, RCX, R8, R9`) chứa 5 tham số đầu.
3. Tham số thứ 10 sẽ nằm ở vị trí thứ $10 - 5 = 5$ trên Stack.
4. CPU trỏ thẳng đến ô nhớ thứ 5 (tính từ đỉnh Stack `RSP`), bốc dữ liệu tại đó lên và xử lý.

### 2. Sự kết hợp hủy diệt với `%n` (Ghi bộ nhớ)
* Thẻ `%n` đếm **tổng số ký tự đã in ra stdout** và ghi con số đó vào bộ nhớ.
* Để tránh làm crash chương trình vì ghi giá trị quá lớn (4 bytes), các Red Teamer sử dụng: `%hn` (2 byte) hoặc **`%hhn`** (1 byte).

**Ví dụ:** `%10$hhn` mang ý nghĩa:
*"Đếm số ký tự nãy giờ đã in ra, trích xuất đúng 1 byte cuối cùng (8-bit thấp nhất) của số đếm đó. Sau đó, chui vào ô nhớ thứ 10 trên Stack (ô nhớ này đang chứa một con trỏ địa chỉ), và ghi 1 byte đó vào địa chỉ đích kia."*

---

## 🧩 Phần 2: Giải phẫu thuật toán cốt lõi của `fmtstr_payload`

Hàm `fmtstr_payload(offset, {target_addr: value})` trong Pwntools là một cỗ máy giải quyết 4 bài toán kiến trúc máy tính cùng lúc. Giả sử ta gọi: `fmtstr_payload(10, {0x404040: 0x6F726568})`.

### 📝 Bài toán 1: Vách ngăn Null-byte trên 64-bit (Memory Layout)
* Trên kiến trúc 64-bit, địa chỉ `0x404040` được lưu thành `0x0000000000404040`.
* Nếu đặt địa chỉ này ở đầu chuỗi payload, byte `0x00` sẽ đánh lừa `printf` rằng chuỗi đã kết thúc (Null-terminator).
* **Giải pháp của Pwntools:** Chia payload làm 2 nửa. Nửa đầu chứa toàn ký tự in ấn (`%c`, `%hhn`). Nửa sau đặt ẩn các địa chỉ (`0x404040`).

[Image of x86_64 stack memory layout for format string vulnerability]

### 📝 Bài toán 2: Chia để trị (Byte Chunking)
* Để ghi số `0x6F726568` (1.8 tỷ hệ thập phân), in 1.8 tỷ khoảng trắng sẽ làm sập kết nối mạng.
* **Giải pháp:** Pwntools xé số này thành 4 byte riêng lẻ theo nguyên tắc Little-Endian và ghi tuần tự vào 4 ô nhớ liên tiếp:
    * `0x68` (104) -> `0x404040`
    * `0x65` (101) -> `0x404041`
    * `0x72` (114) -> `0x404042`
    * `0x6f` (111) -> `0x404043`

### 📝 Bài toán 3: Tính toán cộng dồn & Tràn số (Integer Overflow)
* Vì thẻ `%hhn` đếm tổng số ký tự ĐÃ IN TỪ ĐẦU, bộ đếm này liên tục tăng.
* **Giải pháp:** Lợi dụng tính năng tràn 1 byte (Integer Overflow):
    1. Để ghi `0x68`: Dùng `%104c` (đã in 104 ký tự). `%hhn` bốc byte `0x68`.
    2. Để ghi `0x65` (101): Pwntools tính nhẩm cần vượt qua mốc 255 để vòng lại. Target là `0x165` (357 thập phân).
    3. Cần in thêm: $357 - 104 = 253$ ký tự. Sinh ra `%253c`.
    4. Tổng số ký tự = 357 (`0x0165`). Thẻ `%hhn` chém lấy 1 byte cuối -> Ra chuẩn `0x65`!

### 📝 Bài toán 4: Căn lề Stack (Memory Alignment)
* Stack 64-bit lưu trữ theo từng khối 8 byte.
* Nếu nửa đầu của payload dài một số lẻ (vd: 30 byte), các địa chỉ ở nửa sau sẽ bị trượt khỏi ranh giới 8 byte, dẫn đến con trỏ bị sai lệch.
* **Giải pháp:**
    1. Pwntools đo chiều dài nửa đầu (vd: 30 byte).
    2. Tự động chèn thêm Padding (vd: thêm ký tự `aa`) để tổng thành 32 byte (vừa khít $32 / 8 = 4$ khối Stack).
    3. Cập nhật Offset tĩnh: Offset gốc là `10`, nửa đầu chiếm `4` khối. Vậy các địa chỉ ở nửa sau sẽ nằm bắt đầu từ ô nhớ thứ $10 + 4 = 14$.
    4. Pwntools tự động update toàn bộ thẻ thành `%14$hhn`, `%15$hhn`, v.v.

---

## 💾 3. Cấu trúc Payload thực tế khi nằm trên RAM

Khối dữ liệu cuối cùng được đẩy xuống RAM sẽ có hình thù như sau:


```text
[-- Nửa đầu: 32 bytes (Vừa khít 4 ô nhớ 64-bit) --]
"%104c" + "%14$hhn" + "%253c" + "%15$hhn" + ... + "aa"

[-- Nửa sau: 32 bytes (Chứa 4 địa chỉ) --]
[0x00..404040] [0x00..404041] [0x00..404042] [0x00..404043]

## 1. Dữ liệu Payload thô (Raw Payload)

Khi in payload được tạo ra bởi Pwntools, ta thu được chuỗi byte sau:
b'%101c%16$hhn%3c%17$hhn%7c%18$hhn%3c%19$hhnaaaaaaA@@\x00\x00\x00\x00\x00@@@\x00\x00\x00\x00\x00C@@\x00\x00\x00\x00\x00B@@\x00\x00\x00\x00\x00'
