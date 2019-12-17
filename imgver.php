<?php

$image = $_POST['image'];
$name = $_POST['name'];
$pk = $_POST['pk'];
$path = "$name.jpg";
file_put_contents($path,base64_decode($image));
$var1=shell_exec("python newmerge2_3.py $pk $path 2>&1");
echo "$var1";
unlink($path);
?>

