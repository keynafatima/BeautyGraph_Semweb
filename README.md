# BeautyGraph

BeautyGraph adalah project Semantic Web untuk sistem pencarian produk skincare berbasis **Ontology, RDF, dan SPARQL**. Project ini merepresentasikan produk skincare sebagai knowledge graph yang menghubungkan produk dengan brand, kategori, ingredient, skin type, skin concern, benefit, dan price range.

## Tujuan

Project ini dibuat untuk memenuhi proyek akhir mata kuliah Semantic Web dengan tujuan:

1. Mendesain ontology untuk domain produk skincare.
2. Mengubah data produk skincare menjadi RDF triples.
3. Menjalankan query SPARQL terhadap RDF dataset.
4. Menyediakan SPARQL endpoint.
5. Membangun website pencarian berbasis data semantik.

## Dataset

Dataset awal terdiri dari 50 produk skincare dari 5 kategori:

- Cleanser
- Toner
- Serum
- Moisturizer
- Sunscreen

Kolom utama dataset:

- `product_id`
- `product_name`
- `brand`
- `category`
- `ingredient_1` sampai `ingredient_5`
- `skin_type`
- `concern_1`
- `concern_2`
- `benefit_1`
- `benefit_2`
- `price_range`
- `source_name`
- `source_url`

## Ontology

Class utama:

- `Product`
- `Brand`
- `Category`
- `Ingredient`
- `SkinType`
- `SkinConcern`
- `Benefit`
- `PriceRange`

Object property utama:

- `belongsToBrand`
- `belongsToCategory`
- `hasIngredient`
- `suitableFor`
- `targetsConcern`
- `hasBenefit`
- `hasPriceRange`

Datatype property utama:

- `productName`
- `brandName`
- `ingredientName`
- `sourceName`
- `sourceURL`

## Struktur Folder Rekomendasi

```text
beautygraph/
├── data/
│   ├── raw/
│   │   └── beautygraph_50products.csv
│   ├── ontology/
│   │   └── beautygraph_ontology.ttl
│   └── processed/
│       └── beautygraph.ttl
├── docs/
│   ├── data_dictionary.md
│   ├── project_scope.md
│   └── logbook.md
├── scripts/
│   └── csv_to_rdf.py
├── backend/
│   └── app.py
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
└── README.md
```
