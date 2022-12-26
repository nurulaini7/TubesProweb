<?php
session_start();
$results = $_GET['id'];

if (isset($_SESSION['keranjang'][$results]))
{
    $_SESSION['keranjang'][$results]+=1;
}
else
{
    $_SESSION['keranjang'][$results] = 1;
}

// echo "<pre>";
// print_r($_SESSION);
// echo "</pre>";

// halaman keranjang
echo "<script>alert('Produk anda telah masuk ke keranjang');</script>";
echo "<script>location='index.php';</script>";
?>