<?php
session_start();
$id = $_GET["id"];
unset($_SESSION["keranjang"][$id]);

echo "<script>alert('Produk anda dihapus dari keranjang');</script>";
echo "<script>location='keranjang.php';</script>"

?>