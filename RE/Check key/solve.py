# 1. Chuỗi Key dùng để XOR (Lấy từ code v17)
# Lưu ý: Code gốc có dấu backtick ` ở cuối chuỗi
fake_flag_key = "BKSEC{CHAO_MUN9_D3N_R3V3RS3!!!}`"

# 2. Tính Master Key (XOR tất cả ký tự trong Key lại với nhau)
master_key = 0
for char in fake_flag_key:
    master_key ^= ord(char)

print(f"[*] Master Key calculated: {master_key} (Hex: {hex(master_key)})")

# =================================================================
# QUAN TRỌNG: Bạn phải điền chuỗi Hex lấy từ hàm CheckKey vào đây
# Ví dụ: target_hex = "4567..." (Đây là phần Thịnh phải tìm trong IDA)
# Gợi ý: Nó là chuỗi dài loằng ngoằng trong hàm CheckKey
# =================================================================
target_hex = "636A7264625A76126D62116C127E75117E731277127372120000005C" 

# Nếu bạn chưa tìm thấy trong CheckKey, hãy thử dùng chuỗi này nếu nghi ngờ
# (Đây là giả định dựa trên 28 ký tự input * 2 = 56 ký tự Hex)
# Nhưng tốt nhất hãy vào CheckKey để lấy chuẩn.

def solve():
    if target_hex == "DIEN_CHUOI_HEX_O_DAY":
        print("[!] Lỗi: Bạn chưa điền chuỗi Hex lấy từ hàm CheckKey vào script!")
        return

    print("[*] Decrypting...")
    flag = ""
    
    # Duyệt qua chuỗi Hex, cứ 2 ký tự gom thành 1 byte
    for i in range(0, len(target_hex), 2):
        hex_pair = target_hex[i:i+2]
        # Chuyển Hex thành số nguyên
        val = int(hex_pair, 16)
        
        # Đảo ngược phép toán XOR: Input = Result ^ MasterKey
        original_char = chr(val ^ master_key)
        flag += original_char
        
    print("-" * 30)
    print(f"FLAG CỦA BẠN LÀ: {flag}")
    print("-" * 30)

if __name__ == "__main__":
    solve()