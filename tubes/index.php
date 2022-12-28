<?php 
    require('includes/koneksi.php');
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
    <link rel='stylesheet' href='https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.1/css/all.min.css'>
    <link rel="stylesheet" href="assets/css/style.css" />
    <link href="https://unpkg.com/aos@2.3.1/dist/aos.css" rel="stylesheet">
    <title>Eracom</title>
  
    <!-- icons -->
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
              <a class="nav-link" href="#">Register</a>
            </li>
            <li class="nav-item mt-2">
              <a class="nav-link" href="#">Login</a>
            </li>
            <div class="icons-home nav-icons">
              <a href="keranjang.php"><i class='bx bxs-cart'></i></i></a>
            </div>
            <div class="icons-home nav-icons">
              <a href="includes/search.php"><i class='bx bx-search'></i></a>
            </div>

          </ul>
        </div>
      </div>
    </nav>
    <!-- Akhir Navbar -->

    <!-- carousel-->
   
    <div id="carouselExampleIndicators" class="carousel slide" data-bs-ride="carousel">
      <div class="carousel-indicators">
        <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="0" class="active" aria-current="true" aria-label="Slide 1"></button>
        <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="1" aria-label="Slide 2"></button>
        <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="2" aria-label="Slide 3"></button>
      </div>
      <div class="carousel-inner">
        <div class="carousel-item active" data-bs-interval="1600">
          <img src="assets/img/laptop1.jpg" class="d-block img-fluid w-100 " alt="img1">
        </div>
        <div class="carousel-item" data-bs-interval="1600">
          <img src="assets/img/laptop2.jpg" class="d-block img-fluid w-100 " alt="img2">
        </div>
        <div class="carousel-item" data-bs-interval="1600">
          <img src="assets/img/laptop3.jpg" class="d-block  img-fluid w-100" alt="img3">
        </div>
      </div>

    </div>
  </div>
    <!-- akhir carousel-->


    <!--Awal Produk-->

		<section class="new-arrivals" id="apple">
			<div class="container">
				<div class="text-arrivals row align-items-center">
					<div class="title col-7 col-sm-6 col-md-9 text-left">
						<h3 class="text-main"><span>App</span>le</h3>
					</div>
					<div class="text-show-all col-5 col-sm-6 col-md-3 text-right text-main pr-md-0">
					</div>
				</div>

        
				
				<div class="products row">
					<?php 
            $i = 0;
            foreach($resultMac as $results) :
          ?>
        
          <div class="product col-12 col-sm-12 col-md-6 col-lg-4 col-xl-3 mb-md-4 md-lg-0 mb-sm-4" data-aos="fade-up" data-aos-delay="<?=100*$i?>">
						<div class="bg-white h-100">
							<div class="product-image text-center">
								<img src="assets/img/produk/<?=$results['gambar']?>" alt="<?=$results['nama']?>" class="img-fluid pt-4 px-3">
							</div>
              <div class="desc-product card-body d-flex flex-column">
                <p class="card-title"><?=$results['nama']?></p>
                <p class="text-second card-text price">Rp <?=number_format($results['harga'],'0',',','.')?></p>
                <div class="m-auto" style="color: white;">
                  <a href="beli.php?id=<?php echo $results['id'];?>" class="btn btn-danger my-cart-btn">Add to cart</a>
                  <a href="#" class="btn btn-info btn-white">Detail</a>
                </div>
              </div>

              <!-- <div class="progress mx-5 mb-2" style="height: 5px;">
                <div class="progress-bar bg-danger" style="width: <?=$results['stok']?>" role="progressbar" aria-valuenow="<?=$results['stok']?>" aria-valuemin="0" aria-valuemax="100"></div>
              </div> -->

						</div>
          </div>
        

          <?php 
            $i++;
            endforeach; 
          ?>
				</div>

			</div>
		</section>

   
    <section class="products-section" id="windows">
      
			<div class="container">
				<div class="text-products row align-items-center">
					<div class="title-product col-7 col-sm-6 col-md-9 mt-4">
						<h2 class="text-main"><span>Win</span>dows</h2>
					</div>
					<div class="text-show-all text-right text-main col-5 col-sm-6 col-md-3 pr-md-0">
					</div>
				</div>

				<div class="products row" >

          <?php 
            $i = 0;
            foreach($resultWindows as $results): 
          ?>

					<div  class="product col-12 col-sm-12 col-md-6 col-lg-4 col-xl-3 mb-md-4 md-lg-0 mb-sm-4" data-aos="fade-up" data-aos-delay="<?=100*$i?>">
						<div class="bg-white h-100">
							<div class="product-image text-center">
								<img src="assets/img/produk/<?=$results['gambar']?>" alt="<?=$results['nama']?>" class="img-fluid pt-4 px-3">
							</div>
							<div class="desc-product card-body d-flex flex-column">
									<p class="card-title"><?=$results['nama']?></p>
									<p class="text-second card-text">Rp <?=number_format($results['harga'],'0',',','.')?></p>
									<div class="mt-auto" style="color: white;">
										<a href="beli.php?id=<?php echo $results ['id'] ?>" class="btn btn-danger my-cart-btn">Add to cart</a>
										<a href="#" class="btn btn-info btn-white">Detail</a>
									</div>
							</div>
						</div>
					</div>

          <?php 
            $i++;
            endforeach; 
          ?>
				</div>
			</div>

    

		</section>
    <!-- akhir Produk -->
    
    <!-- Awal Footer -->
     <footer>
      <div class="container">
        <div class="footer-content row mb-4">
          <div class="footer-brand col-12 col-sm-12 col-md-3 col-lg-3">
            <div>
            <img src="assets/img/logo.png" alt="" width="300px" height="100px" />
            <br><br>
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
                  <div class="footer-item-content">
                    <h3 class="text-main">Fitur</h3>
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
<!-- Akhir footer -->
    
    <script src="assets/js/main.js"></script>
    <script src="https://unpkg.com/aos@2.3.1/dist/aos.js"></script>
    <script>
      AOS.init();
    </script>
    
    <!-- Option 1: Bootstrap Bundle with Popper -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>
 
  </body>
</html>
