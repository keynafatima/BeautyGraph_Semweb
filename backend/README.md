# BeautyGraph Backend

Backend ini menyediakan SPARQL Endpoint untuk RDF dataset BeautyGraph.

## Struktur

```text
backend/
├── app.py
├── requirements.txt
└── README.md
```

Backend membaca file RDF dari:

```text
data/processed/beautygraph.ttl
```

## Instalasi

Jalankan dari root project:

```powershell
cd D:\Semweb\BeautyGraph_Semweb
pip install -r backend/requirements.txt
```

Kalau memakai Python path lengkap:

```powershell
cd D:\Semweb\BeautyGraph_Semweb
& C:\Users\ASUS\AppData\Local\Programs\Python\Python312\python.exe -m pip install -r backend/requirements.txt
```

## Menjalankan Backend

```powershell
cd D:\Semweb\BeautyGraph_Semweb
python .\backend\app.py
```

Atau:

```powershell
cd D:\Semweb\BeautyGraph_Semweb
& C:\Users\ASUS\AppData\Local\Programs\Python\Python312\python.exe .\backend\app.py
```

Jika berhasil, backend berjalan di:

```text
http://127.0.0.1:5000
```

## Endpoint

### 1. Health Check

```http
GET /health
```

Contoh:

```text
http://127.0.0.1:5000/health
```

Output berisi status backend, path RDF, total triples, dan total produk.

---

### 2. SPARQL Endpoint via GET

```http
GET /sparql?query=...
```

Contoh query:

```sparql
PREFIX beauty: <http://beautygraph.org/ontology#>

SELECT ?product ?name
WHERE {
  ?product a beauty:Product ;
           beauty:productName ?name .
}
LIMIT 10
```

Contoh akses dari browser harus di-URL encode. Lebih mudah gunakan POST.

---

### 3. SPARQL Endpoint via POST

```http
POST /sparql
Content-Type: application/json
```

Body:

```json
{
  "query": "PREFIX beauty: <http://beautygraph.org/ontology#> SELECT ?product ?name WHERE { ?product a beauty:Product ; beauty:productName ?name . } LIMIT 10"
}
```

---

### 4. Product Search

```http
GET /products
```

Contoh semua produk:

```text
http://127.0.0.1:5000/products
```

Contoh dengan filter:

```text
http://127.0.0.1:5000/products?skin_type=OilySkin&concern=Acne
```

Filter yang tersedia:

| Query Param | Contoh |
|---|---|
| `skin_type` | `OilySkin` |
| `concern` | `Acne` |
| `ingredient` | `Niacinamide` |
| `brand` | `Wardah` |
| `category` | `Serum` |
| `benefit` | `Brightening` |
| `price_range` | `Mid` |

---

### 5. Filter Options

```http
GET /filters
```

Contoh:

```text
http://127.0.0.1:5000/filters
```

Endpoint ini mengembalikan daftar brand, category, ingredient, skin type, concern, benefit, dan price range yang tersedia dalam RDF.

## Catatan

Endpoint `/sparql` adalah bagian paling penting untuk memenuhi requirement Semantic Web karena memungkinkan pengguna mengirim query SPARQL langsung ke RDF dataset BeautyGraph.
