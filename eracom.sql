-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 20, 2022 at 09:49 AM
-- Server version: 10.4.24-MariaDB
-- PHP Version: 8.1.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `eracom`
--

-- --------------------------------------------------------

--
-- Table structure for table `produk`
--

CREATE TABLE `produk` (
  `id` int(11) NOT NULL,
  `nama` varchar(60) NOT NULL,
  `harga` int(9) NOT NULL,
  `stok` int(3) NOT NULL,
  `gambar` varchar(60) NOT NULL,
  `os` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `produk`
--

INSERT INTO `produk` (`id`, `nama`, `harga`, `stok`, `gambar`, `os`) VALUES
(1, 'Apple MacBook Air 2022 M2 Chip 13 Inch', 20000000, 10, 'Apple MacBook Air 2022 M2 Chip 13 Inch.jpg', 'mac'),
(2, 'Apple Macbook Pro 2021 14 M1 Pro', 25000000, 10, 'Apple Macbook Pro 2021 14 M1 Pro.jpg', 'mac'),
(3, 'MacBook Air 2020 13 inch M1 Chip', 25000000, 20, 'MacBook Air 2020 13 inch M1 Chip 8 Core.jpg', 'mac'),
(4, 'Apple MacBook Air 2022 M213 Inch', 25000000, 30, 'MacBook Air 2022 M2 13 Inch.jpg', 'mac'),
(5, 'Lenovo Thinkpad E14-Black-1', 20000000, 30, 'Lenovo-Thinkpad-E14-Black-1.jpg', 'windows'),
(6, 'ASUS Zenbook Flip 13 OLED', 20000000, 40, 'ASUS Zenbook Flip 13 OLED UX363EA-OLED553 - Pine Grey.png', 'windows'),
(7, 'Asus Tuf Gaming f15', 20000000, 5, 'asus tuf gaming f15.png', 'windows'),
(8, 'ASUS ROG Zephyrus G14', 20000000, 3, 'ASUS ROG Zephyrus G14 GA402RJ-R9X6B6G-O - Eclipse Gray.jpg', 'windows');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `produk`
--
ALTER TABLE `produk`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `produk`
--
ALTER TABLE `produk`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
