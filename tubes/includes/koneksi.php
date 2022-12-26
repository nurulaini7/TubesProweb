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
    
?>