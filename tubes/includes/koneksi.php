<?php 
    $conn = mysqli_connect('localhost','root','','eracom');

    if(!$conn){
        die("ERROR: ".mysqli_error());
    }

    function query($query){
        global $conn;
        $results = mysqli_query($conn, $query);
        $rows = [];
        while($row = mysqli_fetch_assoc($results)){
            $rows[] = $row;
        }
        return $rows;
    }

    function search($keyword){
        global $conn;
        $filtered = mysqli_real_escape_string($conn, $keyword);
        $query = "SELECT * FROM produk 
        WHERE nama LIKE '%$filtered%' OR harga LIKE '%$filtered%' OR os LIKE '%$filtered%';";
        
        return query($query);
    }
    
    function delete($id){
        global $conn;
        $result = mysqli_query($conn, "DELETE FROM produk WHERE id = $id");
        if($result === TRUE){
            echo "<script>alert('Penghapusan data berhasil!')</script>";
            echo "<script>location.href= 'produk.php'</script>";
        }else{
            echo "<script>alert('Gagal menghapus data, Silahkan coba lagi !')</script>";
        }
    }

    function insert($data)
    {
        global $conn;
        $nama = $data['nama'];
        $harga = $data['harga'];
        $stok = $data['stok'];
        $os = $data['os'];
        $deskripsi = $data['deskripsi'];

        $gambar = upload(); 
        if(!$gambar){
            return false;
        }

        $query  =  "INSERT INTO produk(nama,harga,stok,os,deskripsi,gambar)
                    VALUES
                    ('$nama',  $harga, $stok, '$os', '$deskripsi', '$gambar')
                ";
        mysqli_query($conn, $query);

        return mysqli_affected_rows($conn);
    }

    function upload(){
        $namafile = $_FILES['gambar']['name'];
        $ukuranfile = $_FILES['gambar']['size'];
        $error = $_FILES['gambar']['error'];
        $tmpName = $_FILES['gambar']['tmp_name'];

        //cek ekstensi gambar yang diupload
        $ekstensigambarvalid = ['jpg', 'jpeg', 'png'];

        //memecah namafile menjadi array
        $ekstensigambar = explode('.',$namafile);

        $ekstensigambar = strtolower(end($ekstensigambar));

        if(!in_array($ekstensigambar, $ekstensigambarvalid)){
            echo "<script>alert('Upload gambar dengan ekstensi jpg, jpeg, atau png!')</script>";
            return false;
        }

        // cek ukuran file
        if($ukuranfile > 10000000){
            echo "<script>alert('Ukuran gambar terlalu besar!')</script>";
            return false;
        }

        $namafilebaru = uniqid();
        $namafilebaru .= '.';
        $namafilebaru .= $ekstensigambar;

        move_uploaded_file($tmpName, '../../assets/img/produk/'.$namafilebaru);
        return $namafilebaru;
    }
        

    function update($data){
        global $conn;
        $id = $data['id'];
        $nama = $data['nama'];
        $harga = $data['harga'];
        $stok = $data['stok'];
        $os = $data['os'];
        $deskripsi = $data['deskripsi'];
        $gambarlama = $data['gambarlama'];

        //jika gambar tidak di upload user
        if($_FILES['gambar'] === 4){
            $gambar = $gambarlama;
        }else{
            $gambar = upload();
        }

        mysqli_query($conn, "UPDATE produk SET 
        nama = '$nama', 
        harga = $harga, 
        stok = $stok, 
        os = '$os',
        deskripsi = '$deskripsi',
        gambar = '$gambar' 
        WHERE id = $id");

        return mysqli_affected_rows($conn);
    }
?>