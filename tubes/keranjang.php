<?php
session_start();

$koneksi = new mysqli ("localhost", "root", "", "eracom");

?>

<!DOCTYPE html>
<html>
<head>
    <title>keranjang</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous" />
    <link rel="stylesheet" href="assets/css/style.css" />
    <link href='https://unpkg.com/boxicons@2.1.4/css/boxicons.min.css' rel='stylesheet'>

</head>
<body>
    <!-- Awal Navbar -->
    <nav class="navbar navbar-expand-lg bg-dark navbar-dark py-2 sticky-top">
      <div class="container-fluid">
        <a class="navbar-brand" href="#">
          <img src="assets/img/logo.png" alt="" width="200px" height="70px" />
        </a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav ms-auto">
            

            <li class="nav-item mt-2">
              <a class="nav-link" href="index.php">Home</a>
            </li>
            <li class="nav-item mt-2">
              <a class="nav-link" href="#">Login</a>
            </li>
            <li class="nav-item mt-2">
              <a class="nav-link" href="#">Register</a>
            </li>
            <div class="icons-home nav-icons">
              <a href=""><i class='bx bxs-cart'></i></i></a>
            </div>
          </ul>
        </div>
      </div>
    </nav>
 <section class="konten bg-white">
    <div class="container">
        <h1>Keranjang Belanja</h1>
        <hr>
        <table class="table table-bordered">
            <thead>
                <tr>
                    <th>No</th>
                    <th>Produk</th>
                    <th>Harga</th>
                    <th>Jumlah</th>
                    <th>Total</th>
                    <th>Aksi</th>
                </tr>
            </thead>
            <tbody>
                <?php $nomor=1 ?>
                <?php foreach ($_SESSION["keranjang"] as $id => $jumlah): ?>
                    <?php
                    $ambil = $koneksi->query("SELECT * FROM produk WHERE id='$id'");
                    $pisah = $ambil->fetch_assoc();
                    $total = $pisah ["harga"]*$jumlah;
                    ?>
                <tr>
                    <td><?php echo $nomor; ?></td>
                    <td><?php echo $pisah ["nama"]; ?></td>
                    <td>Rp.<?php echo number_format($pisah["harga"]);?> </td>
                    <td><?php echo $jumlah; ?></td>
                    <td>Rp.<?php echo number_format($total);?></td>
                    <td>
                        <a href="hapusproduk.php?id=<?php echo $id?>" class="btn btn-danger btn-xs">Hapus</a>
                    </td>
                </tr>
                <?php $nomor++; ?>
                <?php endforeach ?>
            </tbody>
        </table>
                <a href="index.php" class="btn btn-default">Lanjut belanja</a>
                <a href="checkout.php" class="btn btn-primary">checkout</a>

    </div>
 </section>
</body>
</html>
