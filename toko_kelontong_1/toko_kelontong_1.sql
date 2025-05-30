SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

CREATE TABLE `barang` (
  `id` int(11) NOT NULL,
  `nama` varchar(100) NOT NULL,
  `harga` int(11) NOT NULL,
  `stok` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `barang`
--

INSERT INTO `barang` (`id`, `nama`, `harga`, `stok`) VALUES
(1, 'sereal', 5000, 15),
(2, 'Indomie Goreng', 3000, 120),
(3, 'Susu Ultra Milk', 7000, 49),
(4, 'Sabun Lifebuoy', 4000, 80),
(5, 'Beras Ramos 5kg', 65000, 25),
(6, 'Minyak Goreng Bimoli 1L', 16000, 30),
(7, 'Shampoo Sunsilk 170ml', 15000, 35),
(8, 'Teh Botol Sosro', 4000, 60),
(9, 'Kopi Kapal Api', 5000, 100),
(10, 'Roti Sari Roti Tawar', 13000, 40),
(11, 'Gula Pasir 1kg', 14000, 45),
(12, 'Mie Sedap Soto', 2800, 90),
(13, 'Aqua 600ml', 3500, 100),
(14, 'Sabun Nuvo', 4500, 60),
(15, 'Shampoo Clear', 17000, 30),
(16, 'Snack Chitato', 8000, 50),
(17, 'Biskuit Roma Kelapa', 9000, 40),
(18, 'Minyak Tropical 2L', 32000, 20),
(19, 'Pepsodent Pasta Gigi', 9000, 70),
(20, 'Teh Celup Sariwangi', 6000, 40),
(21, 'Telur Ayam (1 Butir)', 2500, 200),
(22, 'Kecap Manis ABC', 18000, 25),
(23, 'Sambal Indofood', 12000, 20),
(24, 'Baterai ABC AA', 8000, 35),
(25, 'Deterjen Rinso', 15000, 30),
(26, 'Pel SuperMop', 25000, 10),
(27, 'Pocari Sweat 500ml', 7000, 50),
(28, 'Kerupuk Udang', 4000, 60),
(29, 'Masker Medis 10pcs', 12000, 25),
(30, 'Tisu Paseo', 11000, 30),
(31, 'Sarden ABC 425gr', 17000, 20),
(32, 'Dancow 400gr', 45000, 15),
(33, 'Qtela Singkong', 7500, 35),
(34, 'Terigu Segitiga Biru', 13000, 40),
(35, 'Garam Dapur 500gr', 4000, 50),
(36, 'SilverQueen Coklat', 15000, 20),
(37, 'Sunlight 800ml', 14000, 35),
(38, 'Buku Tulis Sidu', 3000, 60),
(39, 'Pensil 2B', 2000, 100),
(40, 'Pulpen Standard', 2500, 80),
(41, 'Gas Elpiji 3kg', 22000, 25),
(42, 'Kopi Good Day', 2000, 100),
(43, 'Le Minerale 600ml', 3500, 70),
(44, 'Nabati Coklat', 6000, 60),
(45, 'Mie Gaga 100', 2800, 90),
(46, 'Kacang Garuda', 7000, 50),
(47, 'Tepung Bumbu Sajiku', 5000, 40),
(48, 'Pantene Shampoo', 16000, 30),
(49, 'Baygon Spray', 17000, 20),
(50, 'Mizone Isotonik', 5000, 40),
(51, 'Sikat Gigi Formula', 6000, 50);

-- --------------------------------------------------------

--
-- Struktur dari tabel `detail_pesanan`
--

CREATE TABLE `detail_pesanan` (
  `id` int(11) NOT NULL,
  `pesanan_id` int(11) DEFAULT NULL,
  `barang_id` int(11) DEFAULT NULL,
  `jumlah` int(11) DEFAULT NULL,
  `subtotal` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `pesanan`
--

CREATE TABLE `pesanan` (
  `id` int(11) NOT NULL,
  `tanggal` datetime DEFAULT current_timestamp(),
  `total` int(11) NOT NULL,
  `nama_pelanggan` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


--
-- Indeks untuk tabel `barang`
--
ALTER TABLE `barang`
  ADD PRIMARY KEY (`id`);

--
-- Indeks untuk tabel `detail_pesanan`
--
ALTER TABLE `detail_pesanan`
  ADD PRIMARY KEY (`id`),
  ADD KEY `pesanan_id` (`pesanan_id`),
  ADD KEY `barang_id` (`barang_id`);

--
-- Indeks untuk tabel `pesanan`
--
ALTER TABLE `pesanan`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT untuk tabel yang dibuang
--

--
-- AUTO_INCREMENT untuk tabel `barang`
--
ALTER TABLE `barang`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=52;

--
-- AUTO_INCREMENT untuk tabel `detail_pesanan`
--
ALTER TABLE `detail_pesanan`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT untuk tabel `pesanan`
--
ALTER TABLE `pesanan`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Ketidakleluasaan untuk tabel pelimpahan (Dumped Tables)
--

--
-- Ketidakleluasaan untuk tabel `detail_pesanan`
--
ALTER TABLE `detail_pesanan`
  ADD CONSTRAINT `detail_pesanan_ibfk_1` FOREIGN KEY (`pesanan_id`) REFERENCES `pesanan` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `detail_pesanan_ibfk_2` FOREIGN KEY (`barang_id`) REFERENCES `barang` (`id`);
COMMIT;
