ex = "Deim(yobzoRoA`m\u0089`ESf;xmOkh ]g}8VjFw[x-tG\u008dlaVCr"
list_data = [  -11,
      34,
      -28,
      -8,
      -57,
      -8,
      2,
      3,
      5,
      -17,
      -13,
      -18,
      -53,
      -5,
      0,
      3,
      -19,
      -16,
      -12,
      -6,
      -48,
      10,
      7,
      -19,
      -4,
      -1,
      -67,
      -19,
      -15,
      9,
      -47,
      -14,
      -8,
      -27,
      3,
      -19,
      3,
      -59,
      5,
      -30,
      8,
      33,
      22,
      -6,
      -50,
      0
]

result1 =''
for i in range(len(ex)):
    result1 += chr(ord(ex[i])-list_data[i])
print(result1) #OCuam_u_vemsU_lknfboicpvtgdratnuhoeKK\ur




sect1 = result1[:16]
sect2 = result1[16:44]
sect3 = result1[44:]
result2 = sect3 + sect2 +sect1
print(sect1)  #OCuam_u_vems
print(sect2)  #sU_lknfboicpvtgdratnuhoeKK\
print(sect3)  #ur
print(result2) #ursU_lknfboicpvtgdratnuhoeKK\OCuam_u_vem


s =''
for i in range(len(result2)):
    if i % 3== 0:
        s+= chr(ord(result2[i])-int(i/3))
    elif i % 3 ==2:
        s+= chr(ord(result2[i])-int((i-2)/3))
    else:
        s+= result2[i]
result3 = s
print(result3) #ursT_kind_of_prog_language}BKSEC{java_is_the_w