<?php 
  require('koneksi.php');
  $term = $_GET['term'];
  $query = "SELECT * FROM produk WHERE nama LIKE '%$term%' OR harga LIKE '%$term%' OR os LIKE '%$term%'";
  $result = mysqli_query($conn, $query);

  while ($row = mysqli_fetch_assoc($result)) {
    $suggestion = array(
      "nama" => $row['nama'],
      "harga" => $row['harga'], 
      "os" => $row['os']
    );
    $suggestions[] = $suggestion;
  }

  echo json_encode($suggestions);
?>