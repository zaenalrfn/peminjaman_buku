-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 10, 2024 at 03:01 PM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `peminjaman_buku`
--

-- --------------------------------------------------------

--
-- Table structure for table `peminjam`
--

CREATE TABLE `peminjam` (
  `id_peminjam` int(11) NOT NULL,
  `nama` varchar(225) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `peminjam`
--

INSERT INTO `peminjam` (`id_peminjam`, `nama`) VALUES
(1, 'Zidan');

-- --------------------------------------------------------

--
-- Table structure for table `peminjam_buku`
--

CREATE TABLE `peminjam_buku` (
  `Id_Pinjam_Buku` int(11) NOT NULL,
  `Id_Buku` int(11) NOT NULL,
  `Id_Peminjam` int(11) NOT NULL,
  `waktu_Peminjaman` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `peminjam_buku`
--

INSERT INTO `peminjam_buku` (`Id_Pinjam_Buku`, `Id_Buku`, `Id_Peminjam`, `waktu_Peminjaman`) VALUES
(1, 4534, 1, '2024-01-10');

-- --------------------------------------------------------

--
-- Table structure for table `pinjam_buku`
--

CREATE TABLE `pinjam_buku` (
  `id_buku` int(5) NOT NULL,
  `judul` varchar(255) NOT NULL,
  `tahun_terbit` int(10) NOT NULL,
  `penulis` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `pinjam_buku`
--

INSERT INTO `pinjam_buku` (`id_buku`, `judul`, `tahun_terbit`, `penulis`) VALUES
(4532, 'Belajar dasar Javascript', 2016, 'Zaenal Arifin'),
(4533, 'Belajar dasar PHP', 2016, 'Zidan'),
(4534, 'Belajar dasar Python', 2019, 'Risqi'),
(4535, 'Belajar dasar CSS', 2015, 'Ikhsan'),
(4536, 'Belajar dasar HTML', 2010, 'Yusron');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `peminjam`
--
ALTER TABLE `peminjam`
  ADD PRIMARY KEY (`id_peminjam`);

--
-- Indexes for table `peminjam_buku`
--
ALTER TABLE `peminjam_buku`
  ADD PRIMARY KEY (`Id_Pinjam_Buku`),
  ADD KEY `Id_Buku` (`Id_Buku`),
  ADD KEY `Id_Peminjam` (`Id_Peminjam`);

--
-- Indexes for table `pinjam_buku`
--
ALTER TABLE `pinjam_buku`
  ADD PRIMARY KEY (`id_buku`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `peminjam`
--
ALTER TABLE `peminjam`
  MODIFY `id_peminjam` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `peminjam_buku`
--
ALTER TABLE `peminjam_buku`
  MODIFY `Id_Pinjam_Buku` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `peminjam_buku`
--
ALTER TABLE `peminjam_buku`
  ADD CONSTRAINT `peminjam_buku_ibfk_1` FOREIGN KEY (`Id_Buku`) REFERENCES `pinjam_buku` (`id_buku`),
  ADD CONSTRAINT `peminjam_buku_ibfk_2` FOREIGN KEY (`Id_Peminjam`) REFERENCES `peminjam` (`id_peminjam`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
