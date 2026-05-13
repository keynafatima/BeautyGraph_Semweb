# Project Scope — BeautyGraph

## Judul Project

**BeautyGraph: Sistem Pencarian Semantik Produk Skincare Berbasis Ontology, RDF, dan SPARQL**

## Latar Belakang

Informasi produk skincare umumnya tersedia dalam bentuk teks biasa, seperti nama produk, brand, kategori, kandungan, jenis kulit yang sesuai, masalah kulit yang ditargetkan, manfaat, dan rentang harga. Namun, informasi tersebut belum selalu terhubung secara semantik, sehingga pengguna sering kesulitan menemukan produk yang paling relevan berdasarkan kebutuhan spesifik.

BeautyGraph dibangun untuk merepresentasikan data produk skincare dalam bentuk ontology dan RDF triples. Dengan pendekatan Semantic Web, produk dapat dicari berdasarkan relasi antar entitas, seperti produk dengan ingredient, produk dengan skin type, produk dengan concern, dan produk dengan benefit.

## Problem Statement

Pengguna skincare membutuhkan sistem pencarian yang tidak hanya mencari berdasarkan nama produk, tetapi juga berdasarkan hubungan semantik antara produk, kandungan, jenis kulit, masalah kulit, manfaat, brand, kategori, dan rentang harga.

## Tujuan Project

1. Membangun ontology untuk domain produk skincare.
2. Mengorganisasi data produk skincare menjadi RDF triples.
3. Menyediakan SPARQL endpoint untuk mengakses data RDF.
4. Membangun website pencarian produk skincare berbasis Semantic Web.
5. Menyediakan fitur pencarian berdasarkan relasi semantik, bukan hanya pencarian teks biasa.

## In Scope

| Aspek | Cakupan |
|---|---|
| Domain | Produk skincare |
| Jumlah data awal | 50 produk |
| Kategori produk | Cleanser, Toner, Serum, Moisturizer, Sunscreen |
| Entitas utama | Product, Brand, Category, Ingredient, SkinType, SkinConcern, Benefit, PriceRange |
| Teknologi utama | RDF, RDFS/OWL, SPARQL, Python RDFLib, Flask, HTML/CSS/JavaScript |
| Fitur utama | Search produk berdasarkan skin type, concern, ingredient, brand, category, benefit, dan price range |
| Output | RDF dataset, ontology, SPARQL endpoint, website pencarian, laporan, logbook, draft artikel, presentasi |

## Out of Scope

| Hal yang Tidak Dibahas | Alasan |
|---|---|
| Diagnosis medis kondisi kulit | Sistem bukan pengganti dermatolog atau tenaga medis. |
| Rekomendasi dermatologis profesional | Membutuhkan validasi ahli dan data klinis. |
| Transaksi pembelian produk | Fokus project adalah Semantic Web, bukan e-commerce. |
| Harga real-time | Dataset hanya menggunakan price range. |
| Review pengguna real-time | Dataset bersifat statis untuk kebutuhan project. |
| Gambar produk | Tidak wajib untuk pembuktian RDF, ontology, dan SPARQL. |
| Ingredient lengkap format INCI | Project hanya menggunakan key ingredients utama. |

## Entitas Ontology

| Class | Deskripsi |
|---|---|
| `Product` | Produk skincare yang tersedia dalam dataset. |
| `Brand` | Merek atau produsen produk skincare. |
| `Category` | Kategori produk skincare. |
| `Ingredient` | Kandungan utama atau bahan aktif produk. |
| `SkinType` | Jenis kulit yang cocok untuk produk. |
| `SkinConcern` | Masalah kulit yang ditargetkan produk. |
| `Benefit` | Manfaat utama atau tambahan produk. |
| `PriceRange` | Rentang harga produk. |

## Relasi Ontology

| Object Property | Domain | Range | Makna |
|---|---|---|---|
| `belongsToBrand` | Product | Brand | Produk berasal dari brand tertentu. |
| `belongsToCategory` | Product | Category | Produk termasuk kategori tertentu. |
| `hasIngredient` | Product | Ingredient | Produk memiliki ingredient tertentu. |
| `suitableFor` | Product | SkinType | Produk cocok untuk jenis kulit tertentu. |
| `targetsConcern` | Product | SkinConcern | Produk menargetkan masalah kulit tertentu. |
| `hasBenefit` | Product | Benefit | Produk memiliki manfaat tertentu. |
| `hasPriceRange` | Product | PriceRange | Produk berada pada rentang harga tertentu. |

## Batasan Akademik

BeautyGraph hanya digunakan untuk kebutuhan project akhir Semantic Web. Sistem ini tidak dimaksudkan sebagai alat diagnosis medis atau pengganti konsultasi dermatologis. Data produk perlu dicantumkan sumbernya agar dapat dipertanggungjawabkan dalam laporan dan presentasi.
