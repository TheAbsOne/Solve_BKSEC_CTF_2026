int __fastcall main(int argc, const char **argv, const char **envp)
{
  char v3; // bl
  __int64 v4; // rax
  char v5; // bl
  unsigned __int64 v6; // rbx
  unsigned __int64 v7; // rbx
  char *v8; // rax
  bool v9; // bl
  char *v10; // rax
  char *v11; // rax
  unsigned __int64 v12; // rbx
  char v13; // bl
  _BYTE v15[32]; // [rsp+0h] [rbp-120h] BYREF
  _BYTE v16[32]; // [rsp+20h] [rbp-100h] BYREF
  _BYTE v17[47]; // [rsp+40h] [rbp-E0h] BYREF
  char v18; // [rsp+6Fh] [rbp-B1h] BYREF
  _BYTE v19[32]; // [rsp+70h] [rbp-B0h] BYREF
  _BYTE v20[32]; // [rsp+90h] [rbp-90h] BYREF
  _BYTE v21[32]; // [rsp+B0h] [rbp-70h] BYREF
  _BYTE v22[40]; // [rsp+D0h] [rbp-50h] BYREF
  char *v23; // [rsp+F8h] [rbp-28h]
  int k; // [rsp+104h] [rbp-1Ch]
  int j; // [rsp+108h] [rbp-18h]
  int i; // [rsp+10Ch] [rbp-14h]

  v23 = &v18;
  std::string::basic_string<std::allocator<char>>(v17, "BKSEC{CHAO_MUN9_D3N_R3V3RS3!!!}`", &v18);
  std::__new_allocator<char>::~__new_allocator(&v18);
  std::string::basic_string(v16);
  std::string::basic_string(v15);
  std::operator<<<std::char_traits<char>>(&_TMC_END__, "Enter password: ");
  std::operator>><char>(&std::cin, v15);
  if ( std::string::length(v15) == 28 )
  {
    for ( i = 0; ; ++i )
    {
      v7 = i;
      if ( v7 >= std::string::length(v15) )
        break;
      for ( j = 0; ; ++j )
      {
        v6 = j;
        if ( v6 >= std::string::length(v17) )
          break;
        v3 = *(_BYTE *)std::string::operator[](v15, i);
        v4 = std::string::length(v17);
        v5 = *(_BYTE *)std::string::operator[](v17, v4 - j - 1) ^ v3;
        *(_BYTE *)std::string::operator[](v15, i) = v5;
      }
    }
    for ( k = 0; ; ++k )
    {
      v12 = k;
      if ( v12 >= std::string::length(v15) )
        break;
      v8 = (char *)std::string::operator[](v15, k);
      CanYouCatchMe[abi:cxx11](v19, (unsigned int)*v8);
      v9 = std::string::length(v19) == 1;
      std::string::~string(v19);
      if ( v9 )
      {
        std::string::operator+=(v16, "0");
        v10 = (char *)std::string::operator[](v15, k);
        CanYouCatchMe[abi:cxx11](v20, (unsigned int)*v10);
        std::string::operator+=(v16, v20);
        std::string::~string(v20);
      }
      else
      {
        v11 = (char *)std::string::operator[](v15, k);
        CanYouCatchMe[abi:cxx11](v21, (unsigned int)*v11);
        std::string::operator+=(v16, v21);
        std::string::~string(v21);
      }
    }
    std::string::basic_string(v22, v16);
    v13 = CheckKey(v22);
    std::string::~string(v22);
    if ( v13 )
      std::operator<<<std::char_traits<char>>(&_TMC_END__, "You are handsome");
    else
      std::operator<<<std::char_traits<char>>(&_TMC_END__, "Try again to be handsome");
  }
  std::string::~string(v15);
  std::string::~string(v16);
  std::string::~string(v17);
  return 0;
}