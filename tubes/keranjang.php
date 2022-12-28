<?php
session_start();

$koneksi = new mysqli ("localhost", "root", "", "eracom");
?>

<!DOCTYPE html>
<html>
<head>
    <title>keranjang</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous" />
    <link rel='stylesheet' href='https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.1/css/all.min.css'>
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
            <div class="icons-home nav-icons">
              <a href="includes/search.php"><i class='bx bx-search'></i></a>
            </div>
          </ul>
        </div>
      </div>
    </nav>
 <section class="konten  text-light mt-5">
    <div class="container mt-6">
        <h1 class="text-center mt-5"><b>Keranjang Belanja</h1>
        <hr>
        <table class="table table-bordered mb-5 bold text-light">
            <thead>
                <tr>
                    <th>No</th>
                    <th>Produk</th>
                    <th>Nama</th>
                    <th>Harga</th>
                    <th>Jumlah</th>
                    <th>Total</th>
                    <th>Aksi</th>
                </tr>
            </thead>
            <tbody>
                <?php
                if(isset($_SESSION['keranjang'])){
                  $nomor=1;  
                  foreach ($_SESSION["keranjang"] as $id => $jumlah): 
                  ?>
                    <?php
                    $ambil = $koneksi->query("SELECT * FROM produk WHERE id='$id'");
                    $pisah = $ambil->fetch_assoc();
                    $total = $pisah ["harga"]*$jumlah;
                    ?>
                <tr>
                    <td><?php echo $nomor; ?></td>
                    <td><img src="assets/img/produk/<?= $pisah["gambar"] ?>" width="50"></td>
                    <td><?php echo $pisah ["nama"]; ?></td>
                    <td>Rp.<?php echo number_format($pisah["harga"]);?> </td>
                    <td><?php echo $jumlah; ?></td>
                    <td>Rp.<?php echo number_format($total);?></td>
                    <td>
                        <a href="hapusproduk.php?id=<?php echo $id?>" class="btn btn-danger btn-xs" onclick="return confirm('Apakah Anda yakin ingin menghapus produk dari keranjang?')">Hapus</a>
                    </td>
                </tr>
                <?php
                  $nomor++;
                  endforeach; }
                  ?>
            </tbody>
        </table>
                <a href="index.php" class="btn btn-primary mb-5">Lanjut belanja</a>
                <a href="checkout.php" class="btn btn-primary mb-5">checkout</a>

    </div>
 </section>



  <!-- Awal Footer -->
 <footer>
      <div class="container">
        <div class="footer-content row mb-4">
          <div class="footer-brand col-12 col-sm-12 col-md-3 col-lg-3">
            <div>
            <h3 class="text-main mb-4 text-white">About</h3>
            <img src="assets/img/logo.png" alt="" width="300px" height="100px" />
            <br><br><br>
            <h6 class="text-white">Eracom merupakan website toko online yang menjual perangkat elektronik berupa laptop, kami menyediakan kebutuhan anda pada era industri 4.0 </h6>
            <br><br> 
            <div class="color-white">
              <a href="" class="me-4 link-secondary">
                <i class="fab fa-facebook-f"></i>
              </a>
              <a href="" class="me-4 link-secondary">
                <i class="fab fa-twitter"></i>
              </a>
              <a href="" class="me-4 link-secondary">
                <i class="fab fa-google"></i>
              </a>
              <a href="" class="me-4 link-secondary">
                <i class="fab fa-instagram"></i>
              </a>
              <a href="" class="me-4 link-secondary">
                <i class="fab fa-github"></i>
              </a>
            </div>
            <div class="col-lg-4 col-md-6 mb-4 mb-md-0">
          </div>
          </div>
          </div>
  
          <div class="footer-items-box col-12 col-sm-12 col-md-9 col-lg-9">
            <div class="footer-items row">
              <div class="footer-item col-12 col-sm-12 col-md-4">
                <div>
                  <div class="footer-item-content me-4">
                    <h3 class="text-main ">Fitur</h3>
                    <p>Home</p>
                    <p>Kategori Produk</a></p>
                    <p>Keranjang</a></p>
                    <p>Register</a></p>
                    <p>Login</a></p>
                    <p>Pencarian</a></p>
                  </div>
                </div>
              </div>
    
                      <div class="col-lg-4 col-md-6 mb-4 mb-md-0">
                        <h5 class="text-uppercase mb-4 text-white">Kontak Kami</h5>
                        <ul class="fa-ul text-white" style="margin-left: 1.65em;">
                          <li class="mb-3">
                            <span class="fa-li"><i class="fas fa-home"></i></span><span class="ms-2">Medan, 00-967, Sumatera Utara</span>
                          </li>
                          <li class="mb-3">
                            <span class="fa-li"><i class="fas fa-envelope"></i></span><span class="ms-2">Eracom22@gmail.com</span>
                          </li>
                          <li class="mb-3">
                            <span class="fa-li"><i class="fas fa-phone"></i></span><span class="ms-2">+62 8123 456 789</span>
                          </li>
                        </ul>
                      </div>

                            <div class="col-lg-4 col-md-6 mb-4 mb-md-0">
                            <h5 class="text-uppercase mb-4 text-white">Jam Operasional</h5>

                            <table class="table text-center text-white">
                              <tbody class="fw-normal">
                                <tr>
                                  <td>Mon - Thu:</td>
                                  <td>8am - 9pm</td>
                                </tr>
                                <tr>
                                  <td>Fri - Sat:</td>
                                  <td>8am - 9pm</td>
                                </tr>
                                <tr>
                                  <td>Sunday:</td>
                                  <td>9am - 10pm</td>
                                </tr>
                              </tbody>
                            </table>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                </div>
              </div>
                      
              <div class="copyright-section border-top">
                <div class="row">
                  <div class="col-12">
                    <div class="copyright-content text-center mt-4">
                      <p class="text-second">Eracom Online Store Copyright &copy; 2022 All Rights Reserved</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </footer>

    <!-- akhir footer -->
</body>
</html>
