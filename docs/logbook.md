# Logbook Project — BeautyGraph

| Tanggal | Kegiatan | Output | PIC |
|---|---|---|---|
| 13 Mei 2026 | Menentukan ide project BeautyGraph sebagai sistem pencarian semantik produk skincare. | Judul dan konsep awal project. | Berdua |
| 13 Mei 2026 | Menentukan scope dataset produk skincare. | Scope 50 produk dari kategori Cleanser, Toner, Serum, Moisturizer, dan Sunscreen. | Berdua |
| 13 Mei 2026 | Menyusun dataset awal produk skincare. | File `beautygraph_50products.csv`. | Anggota Dataset/Frontend |
| 13 Mei 2026 | Mendesain ontology awal. | File `beautygraph_ontology.ttl`. | Anggota Semantic/Backend |
| 13 Mei 2026 | Melakukan review kualitas dataset dan ontology. | Ditemukan typo `UnvenSkinTone`, nilai `DullSkin` pada `skin_type`, dan kebutuhan kolom sumber data. | Berdua |
| 13 Mei 2026 | Membersihkan dataset Fase 1. | File `beautygraph_50products_clean.csv`. | Anggota Dataset/Frontend |
| 13 Mei 2026 | Memperbaiki ontology Fase 1. | File `beautygraph_ontology_clean.ttl`. | Anggota Semantic/Backend |
| 13 Mei 2026 | Membuat dokumentasi Fase 1. | File `data_dictionary.md`, `project_scope.md`, `README.md`, dan `logbook.md`. | Berdua |

## Catatan Lanjutan

Kolom `source_name` dan `source_url` sudah disiapkan, tetapi nilai detailnya perlu diisi berdasarkan sumber produk yang benar, misalnya Sociolla, website resmi brand, atau katalog produk resmi. Jangan mengisi URL yang belum diverifikasi.

| 13 Mei 2026 | Mengisi source_name dan source_url berdasarkan halaman produk asli/terdekat yang ditemukan | beautygraph_50products_sourced.csv dan source audit | Berdua |
