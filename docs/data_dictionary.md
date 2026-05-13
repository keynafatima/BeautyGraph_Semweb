# Data Dictionary — BeautyGraph

Dokumen ini menjelaskan struktur dataset produk skincare yang digunakan pada project **BeautyGraph**.

## Ringkasan Dataset

| Komponen | Jumlah |
|---|---:|
| Produk | 50 |
| Brand unik | 8 |
| Kategori produk | 5 |
| Ingredient unik | 23 |
| Skin type unik | 7 |
| Skin concern unik | 15 |
| Benefit unik | 13 |
| Price range | 2 |

## Struktur Kolom

| Kolom | Tipe Data | Contoh | Keterangan |
|---|---|---|---|
| `product_id` | String | `P001` | ID unik untuk setiap produk. |
| `product_name` | String | `Niacinamide Serum 10%` | Nama produk skincare. |
| `brand` | String | `Somethinc` | Nama brand produk. |
| `category` | Controlled vocabulary | `Serum` | Kategori produk: Cleanser, Toner, Serum, Moisturizer, Sunscreen. |
| `ingredient_1` | String | `Niacinamide` | Kandungan utama pertama. |
| `ingredient_2` | String | `Hyaluronic Acid` | Kandungan utama kedua. |
| `ingredient_3` | String | `Centella Asiatica` | Kandungan utama ketiga. |
| `ingredient_4` | String | `Vitamin C` | Kandungan utama keempat; boleh kosong. |
| `ingredient_5` | String | `Panthenol` | Kandungan utama kelima; boleh kosong. |
| `skin_type` | Multi-value string | `OilySkin\|CombinationSkin` | Jenis kulit yang cocok untuk produk. Dipisahkan dengan `|` jika lebih dari satu. |
| `concern_1` | Multi-value string | `Acne\|LargePores` | Masalah kulit yang menjadi target utama. |
| `concern_2` | Multi-value string | `AcneMarks` | Masalah kulit tambahan; boleh kosong. |
| `benefit_1` | Controlled vocabulary | `Brightening` | Manfaat utama produk. |
| `benefit_2` | Controlled vocabulary | `PoreCare` | Manfaat tambahan; boleh kosong. |
| `price_range` | Controlled vocabulary | `Budget` | Rentang harga produk: Budget, Mid, Premium. |
| `source_name` | String | `Sociolla` | Nama sumber data produk. Kolom ini disiapkan untuk validasi sumber. |
| `source_url` | URL/String | `https://...` | URL sumber data produk. Kolom ini tidak diisi otomatis agar tidak mengarang sumber. |

## Controlled Vocabulary

### Category

- `Cleanser`
- `Moisturizer`
- `Serum`
- `Sunscreen`
- `Toner`

### Skin Type

- `AcneProneSkin`
- `AllSkinTypes`
- `CombinationSkin`
- `DrySkin`
- `NormalSkin`
- `OilySkin`
- `SensitiveSkin`

Catatan: `DullSkin` sudah dihapus dari `skin_type` karena lebih tepat direpresentasikan sebagai concern `Dullness`, bukan jenis kulit.

### Skin Concern

- `Acne`
- `AcneMarks`
- `Aging`
- `Dehydration`
- `Dryness`
- `Dullness`
- `FineLine`
- `Hyperpigmentation`
- `Inflammation`
- `Irritation`
- `LargePores`
- `Redness`
- `Sensitivity`
- `SunDamage`
- `UnevenSkinTone`

Catatan: typo `UnvenSkinTone` sudah diperbaiki menjadi `UnevenSkinTone`.

### Benefit

- `AcneTreatment`
- `AntiAging`
- `BarrierRepair`
- `Brightening`
- `Cleansing`
- `EvenSkinTone`
- `Exfoliating`
- `Hydrating`
- `MattifyingEffect`
- `PoreCare`
- `Repairing`
- `Soothing`
- `SunProtection`

### Price Range

- `Budget`
- `Mid`

## Aturan Cleaning Data

1. Gunakan format PascalCase untuk URI/controlled vocabulary, misalnya `OilySkin`, `AcneMarks`, dan `UnevenSkinTone`.
2. Nilai multi-value dipisahkan menggunakan karakter `|`.
3. Nilai kosong diperbolehkan untuk `ingredient_4`, `ingredient_5`, `concern_2`, `benefit_2`, `source_name`, dan `source_url`.
4. Jangan mengisi `source_url` dengan link yang belum diverifikasi.
5. Dataset ini akan dikonversi menjadi RDF triples pada Fase 2 menggunakan script Python RDFLib.


## Kolom Source Tambahan

- `source_name`: nama website/sumber data produk, misalnya official website brand, SOCO/Sociolla, Female Daily, Watsons, atau retailer tepercaya.
- `source_url`: URL halaman produk atau halaman katalog resmi yang digunakan sebagai dasar data produk.
