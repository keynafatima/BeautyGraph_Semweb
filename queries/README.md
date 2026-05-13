# BeautyGraph SPARQL Queries

Folder ini berisi 7 query SPARQL untuk menguji RDF dataset BeautyGraph.

## Daftar Query

1. `q1_search_by_skin_type.rq`  
   Mencari produk berdasarkan jenis kulit, contoh: `OilySkin`.

2. `q2_search_by_concern.rq`  
   Mencari produk berdasarkan masalah kulit, contoh: `AcneMarks`.

3. `q3_search_by_ingredient.rq`  
   Mencari produk berdasarkan ingredient, contoh: `Niacinamide`.

4. `q4_search_by_brand.rq`  
   Menampilkan produk dari brand tertentu, contoh: `Wardah`.

5. `q5_search_by_skin_type_and_concern.rq`  
   Mencari produk berdasarkan kombinasi jenis kulit dan concern, contoh: `OilySkin + Acne`.

6. `q6_search_by_price_and_benefit.rq`  
   Mencari produk berdasarkan price range dan benefit, contoh: `Mid + Brightening`.

7. `q7_similar_products.rq`  
   Mencari produk yang mirip dengan `P001` berdasarkan shared ingredients.

## Cara Menggunakan

Letakkan folder ini di root project:

```text
BeautyGraph_Semweb/
├── data/
├── scripts/
└── queries/
```

Query dapat dijalankan melalui RDFLib, SPARQL endpoint Flask, atau halaman SPARQL Demo pada website.
