```bash
==========
WEB SITES
==========
https://www.w3schools.com/xml/xpath_syntax.asp
https://www.exploit-db.com
Google dork website https://www.exploit-db.com/google-hacking-database
Wiki site https://en.wikipedia.org/wiki/Google_hacking
=====================
Methodology
=====================
host discovery
host enum ( port scanning )
host interr ( banner grabbing )

Web servers
--script http-enum
interact with the website normally
view page source

=====================
Scrapping with Python
=====================
(Install if needed)
apt install python3-pip
pip3 install lxml
pip3 install requests
--------------------------

import lxml.html
import requests

page = requests.get('http://quotes.toscrape.com')
tree = lxml.html.fromstring(page.content)

authors = tree.xpath('//small[@class="author"]/text()')

print ('Authors: ',authors)


==============
HOST DISCOVERY
==============
for i in {2..254} ;do (ping -c 1 192.168.28.$i | grep "bytes from" &) ;done
for i in {1..254} ;do (ping -c 1 192.168.28.$i | grep "bytes from" &) ;done | awk '{ print $4 }' | sed 's/://g'


Can help Identify a box based on the ping response
128 = windows
64 = some type of nix
60 = mac
255 = solaris

-------------------------------

Port enum
proxychains nmap -sT -Pn -iL ips --open
proxychains nmap -sT -Pn -iL ips -p 1-5000 --open
proxychains nmap -sT -Pn 192.168.28.120 --open
proxychains nmap -sT -Pn 192.168.28.111 -p 80 --script http-enum
proxychains nmap -sT -Pn 192.168.28.111 -p 445 --script smb-os-discovery


----------------------------------

=====================
Nmap Scripts location
=====================

Located in /usr/share/nmap/scripts

Ls -la . | grep "smb*"  ( show all possible smb scripts)

```

