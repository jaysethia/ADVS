<?php
$name = $_POST['name'];
$pk = $_POST['pk'];
$bar = $_POST['bar'];
$path = "$name.xml";
$xfile=fopen("$path","w");
fwrite($xfile,$bar);

$ex="python qr2.py $pk $path 2>&1";
$var1=shell_exec($ex);
unlink($path);
echo $var1;
?>

