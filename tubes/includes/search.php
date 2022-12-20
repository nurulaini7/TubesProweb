<?php 
    require('koneksi.php');
    $resultMac = query("SELECT * FROM produk WHERE os = 'mac'");
    $resultWindows = query("SELECT * FROM produk WHERE os = 'windows'");
?>


<!DOCTYPE html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />

    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous" />
    <link rel="stylesheet" href="../assets/css/style.css" />
    <link href="https://unpkg.com/aos@2.3.1/dist/aos.css" rel="stylesheet">
    <title>Search</title>
  

    <!-- Icons -->
    <link href='https://unpkg.com/boxicons@2.1.4/css/boxicons.min.css' rel='stylesheet'>


  </head>
  <body>
    <!-- Awal Navbar -->
    <nav class="navbar navbar-expand-lg bg-dark navbar-dark py-2 sticky-top">
        <div class="container-fluid">
            <a class="navbar-brand" href="#">
            <img src="../assets/img/logo.png" alt="" width="200px" height="70px" />
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <ul class="navbar-nav ms-auto">
                

                <li class="nav-item mt-2">
                <a class="nav-link" href="../index.php">Home</a>
                </li>
                <li class="nav-item dropdown mt-2">
                <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false"> Kategori </a>
                <ul class="dropdown-menu" aria-labelledby="navbarDropdown">
                    <li><a class="dropdown-item" href="#windows">Windows</a></li>
                    <li><a class="dropdown-item" href="#apple">MacOs</a></li>
                </ul>
                <li class="nav-item mt-2">
                    <a class="nav-link" href="#">About</a>
                </li>
                </li>
                <li class="nav-item mt-2">
                <a class="nav-link" href="#">Login</a>
                </li>
                <li class="nav-item mt-2">
                <a class="nav-link" href="#">Register</a>
                </li>
                <div class="icons-home nav-icons">
                <a href="#"><i class='bx bx-shopping-bag ms-2'></i></a>
                </div>
                <div class="icons-home nav-icons">
                <a href="search.php"><i class='bx bx-search'></i></a>
                </div>

            </ul>
            </div>
        </div>
    </nav>
    <!-- Akhir Navbar -->

   


    <!--Awal search-->
		<section class="new-arrivals">
      <div class="container">
        <div class="search-div">
          <form action="">
            <input type="text">
            <button type="submit" class="icons-home nav-icons"><i class='bx bx-search'></i></button>
          </form>
        </div>
      </div>
		</section>

    <!-- akhir search -->
    
    <!-- Awal Footer -->
    <footer>        
      <div class="container">
        <div class="footer-content row mb-4">
          <div class="footer-brand col-12 col-sm-12 col-md-3 col-lg-3">
            <div>
              <h1 class="text-main">ERACOM</h1>
            </div>
          </div>
  
          <div class="footer-items-box col-12 col-sm-12 col-md-9 col-lg-9">
            <div class="footer-items row">
              <div class="footer-item col-12 col-sm-12 col-md-4">
                <div>
                  <div class="footer-item-content">
                    <h3 class="text-main">Anggota Kelompok</h3>
                    <p>Hanzel Oclihar Tjiam</p>
                    <p>Umar Hilmi</a></p>
                    <p>Nurul Aini</a></p>
                    <p>Annisa Cahyani</a></p>
                    <p>Jungjungan Hans Aryanta Silitonga</a></p>
                    <p>Firman Ramadhani Yusma</a></p>
                  </div>
                </div>
              </div>
    
              <div class="footer-item col-12 col-sm-12 col-md-4">
                <div>
                  <div class="footer-item-content">
                    <h3 class="text-main">Business</h3>
                    <p><a href="#">eracom22@gmail.com</a></p>
                    <p><a href="#">021-1234-5678</a></p>
                    <p><a href="#">Medan, Sumatera Utara</a></p>
                  </div>
                </div>
              </div>
    
              <div class="footer-item col-12 col-sm-12 col-md-4">
                <div>
                  <div class="footer-item-content">
                    <h3 class="text-main">About</h3>
                    
                      <p>Lorem ipsum dolor, sit amet consectetur adipisicing elit. Dolorem fuga laboriosam deserunt culpa, eius magnam adipisci veritatis consectetur cupiditate iusto amet incidunt sapiente nobis sed, nihil labore! Harum, deleniti repellendus!</p>
                    
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


    
    <script src="../assets/js/main.js"></script>
    <script src="https://unpkg.com/aos@2.3.1/dist/aos.js"></script>

    <script>
      AOS.init();
    </script>
    
    <!-- Option 1: Bootstrap Bundle with Popper -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>
  </body>
</html>

