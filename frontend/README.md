# BeautyGraph Frontend

Frontend ini adalah website pencarian untuk project BeautyGraph.

## Fitur

- Semantic search berbasis filter:
  - Skin Type
  - Concern
  - Ingredient
  - Brand
  - Category
  - Benefit
  - Price Range
- Result card produk
- Detail semantik produk
- Knowledge Graph view sederhana untuk setiap produk
- SPARQL Demo page untuk menjalankan query manual ke endpoint `/sparql`
- About RDF/Ontology page

## Struktur

```text
frontend/
├── index.html
├── styles.css
├── app.js
└── README.md
```

## Prasyarat

Backend Flask harus sudah berjalan di:

```text
http://127.0.0.1:5000
```

Jalankan backend dari root project:

```powershell
cd D:\Semweb\BeautyGraph_Semweb
python .\backend\app.py
```

## Cara Menjalankan Frontend

Buka terminal baru, lalu jalankan:

```powershell
cd D:\Semweb\BeautyGraph_Semweb\frontend
python -m http.server 5500
```

Kemudian buka browser:

```text
http://127.0.0.1:5500
```

## Endpoint yang Dipakai

Frontend memakai endpoint backend berikut:

| Endpoint | Fungsi |
|---|---|
| `GET /health` | Mengecek status backend dan jumlah RDF triples |
| `GET /filters` | Mengambil opsi dropdown filter |
| `GET /products` | Mengambil produk berdasarkan filter |
| `POST /sparql` | Menjalankan query SPARQL manual dan detail produk |

## Catatan

Jika halaman menampilkan error backend, pastikan:

1. Backend Flask masih berjalan.
2. URL backend di `app.js` benar:
   ```js
   const API_BASE = "http://127.0.0.1:5000";
   ```
3. File RDF `data/processed/beautygraph.ttl` sudah ada.
