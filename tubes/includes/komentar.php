<?php
    $servername = "localhost";
    $username = "root";
    $password = "";
    $dbname = "eracom";

    $conn = new mysqli($servername, $username, $password, $dbname);
    if ($conn->connect_error){
        die("koneksi terputus: " . $conn->connect_error);
    }
?>