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
    
?>