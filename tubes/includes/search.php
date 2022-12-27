<?php 
  require('koneksi.php');
  $result = query("SELECT * FROM produk");
  if(isset($_POST['search'])){
      $result = search($_POST['keyword']);
  }
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
    <link href = "https://code.jquery.com/ui/1.10.4/themes/ui-lightness/jquery-ui.css" rel = "stylesheet">
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
                  <a href="keranjang.php"><i class='bx bxs-cart'></i></i></a>
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
		<section>
      <div class="container-fluid">
        <div class="box">
          <form action="" method="POST" onsubmit="window.location.href = '#showproducts'">
            <div class="searchbox">
              <input type="text" class="inp" placeholder="Masukkan kata kunci..." name="keyword" id="autocomplete">
              <button class="search-btn" name="search" id="exe">
                <i class="bx bx-search"></i>
              </button>
            </div>
          </form>
        </div>
     </div>
		</section>

    <!-- akhir search -->
    

    <!-- tampilan produk  -->
    
     <section class="products-section" id="showproducts">
      
			<div class="container">
				<div class="text-products row align-items-center">
					<div class="title-product col-7 col-sm-6 col-md-9 mt-4">
						<h2 class="text-main"><span>Semua Produk</span></h2>
					</div>
					<div class="text-show-all text-right text-main col-5 col-sm-6 col-md-3 pr-md-0">
					</div>
				</div>

				<div class="products row" >

          <?php 
            if($result != null){
              $i = 0;
              foreach($result as $results):
          ?>

					<div class="product col-12 col-sm-12 col-md-6 col-lg-4 col-xl-3 mb-md-4 md-lg-0 mb-sm-4" data-aos="fade-up" data-aos-delay="<?=100*$i?>" data-aos-once="true">
						<div class="bg-white h-100">
							<div class="product-image text-center">
								<img src="../assets/img/produk/<?=$results['gambar']?>" alt="<?=$results['nama']?>" class="img-fluid pt-4 px-3">
							</div>
							<div class="desc-product card-body d-flex flex-column">
									<p class="card-title"><?=$results['nama']?></p>
									<p class="text-second card-text">Rp <?=number_format($results['harga'],'0',',','.')?></p>
									<div class="mt-auto">
										<button class="btn btn-danger my-cart-btn">Add to cart</button>
										<a href="#" class="btn btn-info btn-white">Detail</a>
									</div>
							</div>
						</div>
					</div>

          <?php 
            
            $i++;
            endforeach;}
            else{
                echo "<h2 style='color: white;'>PRODUK TIDAK DITEMUKAN</h2>";
                echo "<p style='color: white; font-size: 25px;'>Silahkan coba kata kunci lain</p>";
            } 
          
          ?>

				</div>
			</div>
		</section>

    
    <!-- akhir tampilan produk  -->


   


    
    <script src="https://unpkg.com/aos@2.3.1/dist/aos.js"></script>
    <script src="../assets/js/main.js"></script>

    <script>
      AOS.init();
    </script>
    
    <!-- Option 1: Bootstrap Bundle with Popper -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>
    <script src = "https://code.jquery.com/jquery-1.10.2.js"></script>
    <script src = "https://code.jquery.com/ui/1.10.4/jquery-ui.js"></script>

  </body>
</html>

