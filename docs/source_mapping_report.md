# BeautyGraph Source Mapping Report

Dokumen ini menjelaskan pengisian `source_name` dan `source_url` untuk dataset BeautyGraph. Link yang digunakan berasal dari official brand website, official catalog, SOCO/Sociolla, Female Daily, Watsons, atau retailer tepercaya ketika halaman produk official tidak ditemukan dari hasil pencarian web.

## Ringkasan

- Jumlah produk: 50
- Exact/strong product match: 25
- Closest available source match: 25
- Semua baris sudah memiliki `source_name` dan `source_url`.

## Catatan Penting

Beberapa nama produk pada CSV awal bersifat generik atau tidak sama persis dengan nama produk yang tersedia di halaman brand resmi. Untuk menjaga integritas akademik, file audit menandai baris tersebut sebagai `close`, bukan `exact`. Jika ingin dataset 100% presisi, tahap berikutnya sebaiknya menyamakan `product_name` dengan nama produk asli dari `source_url`.

## Audit Source per Produk

| ID | Product Name di CSV | Source Name | Match | Source URL | Catatan |
|---|---|---|---|---|---|
| P001 | Niacinamide Serum 10% | SOCO Review | close | https://review.soco.id/product/face-serum/70514-niacinamide-moisture-beet-serum | Original name generic; matched to Somethinc Niacinamide + Moisture Beet Serum page. |
| P002 | Aloe Soothing Gel | Somethinc Official | close | https://somethinc.com/id/product/detail/calm-down-skinpair-r-cover-cream | Original name Aloe Soothing Gel not found as exact Somethinc product; matched to official soothing moisturizer product. |
| P003 | Hyaluronic Acid Serum | Somethinc Official | exact | https://somethinc.com/id/product/detail/hyaluronic9-advanced-b5-serum | Matched to official Hyaluronic9+ Advanced + B5 Serum page. |
| P004 | Level 1-2-3 Retinol Serum | Somethinc Official | exact | https://somethinc.com/id/product/detail/level-1-encapsulated-retinol | Matched to official Level 1% Encapsulated Retinol page. |
| P005 | Sunscreen Matte Finish SPF50 | Somethinc Official | close | https://somethinc.com/id/product/detail/holyshield-watery-sunscreen-gel-spf-50-pa | Original name generic Matte Finish SPF50; matched to official Holyshield Watery Sunscreen Gel SPF50+ PA++++. |
| P006 | Acne Spot Gel | Somethinc Official | exact | https://somethinc.com/id/product/detail/acne-shot-ac-spot-gel | Matched to official Acne Shot AC Spot Gel page. |
| P007 | Even Skin Tone Serum | Somethinc Official | close | https://somethinc.com/en/product/detail/gentle-bright-niacinamide-alpha-arbutin-serum | Original name Even Skin Tone Serum; matched to official Gentle Bright Niacinamide + Alpha Arbutin Serum. |
| P008 | Moisturizing Gel Cream | Somethinc Official | close | https://somethinc.com/id/product/detail/ceramic-skin-saviour-moisturizer-gel-reformulated | Original name Moisturizing Gel Cream; matched to official Ceramic Skin Saviour Moisturizer Gel. |
| P009 | White Secret Brightening Serum | Female Daily Review | close | https://reviews.femaledaily.com/products/treatment/serum-essence/wardah/crystal-secret-dark-spot-brightening-serum | Original White Secret line appears older/generic; matched to Wardah Crystal Secret Dark Spot & Brightening Serum. |
| P010 | Hydrating Toner | Wardah Official | close | https://www.wardahbeauty.com/id/product/skincare/nature-daily-hydramild-toner-essence | Original generic Hydrating Toner; matched to official Nature Daily Hydramild Toner Essence. |
| P011 | Acne Care Facial Wash | Wardah Official | exact | https://www.wardahbeauty.com/en/product/skincare/wardah-acnederm-pure-foaming-cleanser | Matched to official Wardah Acnederm Pure Foaming Cleanser page. |
| P012 | Moisturizing Sunscreen SPF40 | Wardah Official | close | https://www.wardahbeauty.com/en/product/skincare/uv-shield-aqua-fresh-sunscreen-serum-spf-50-pa | Original SPF40 name not found; matched to official UV Shield Aqua Fresh Essence SPF50 PA++++. |
| P013 | Lightening Serum | Wardah Official | exact | https://www.wardahbeauty.com/en/product/skincare/ightening-serum-ampoule | Matched to official Lightening Serum Ampoule page. |
| P014 | Hydro Series Moisturizer | Wardah Official | close | https://www.wardahbeauty.com/id/product/skincare/wardah-hydra-rose-moisture-rich-night-gel | Original Hydro Series Moisturizer; matched to official Hydra Rose Moisture Rich Night Gel. |
| P015 | Perfect Bright Toner | Wardah Official | close | https://www.wardahbeauty.com/id/product/skincare/wardah-lightening-face-toner | Original Perfect Bright Toner; matched to official Wardah Lightening Face Toner. |
| P016 | Brightly Ever After Serum | Scarlett Official | exact | https://scarlettofficial.id/product/scarlett-brightly-ever-after-serum | Matched to official Scarlett Brightly Ever After Serum page. |
| P017 | Acne Serum | Scarlett Official | exact | https://scarlettofficial.id/product/scarlett-acne-serum---niacinamide-5--serum | Matched to official Scarlett Acne Serum bundle/source page. |
| P018 | Facial Wash Brightening | Scarlett Official | exact | https://scarlettofficial.id/product/scarlett-brightening-facial-wash | Matched to official Scarlett Brightening Facial Wash page. |
| P019 | Moisturizer Brightening | Scarlett Official | close | https://scarlettofficial.id/product/scarlett-glow-bright-gel-moisturizer---brightening-facial-wash | Original Moisturizer Brightening; matched to official Glow Bright Gel Moisturizer bundle/source page. |
| P020 | UV Shield Moisturizer SPF30 | Scarlett Official | close | https://scarlettofficial.id/product/scarlett-ultra-light-daily-sunscreen-30ml | Original UV Shield Moisturizer SPF30; matched to official Ultra Light Daily Sunscreen SPF50+. |
| P021 | Acne Facial Wash | Scarlett Official | close | https://scarlettofficial.id/product/scarlett-acne-series | Original Acne Facial Wash; matched to official Scarlett Acne Series source page. |
| P022 | Retinol Serum | Scarlett Official | exact | https://scarlettofficial.id/product/scarlett-skin-smoothing-retinol-serum | Matched to official Scarlett Skin Smoothing Retinol Serum page. |
| P023 | Acne Facial Wash | Emina Official | close | https://www.eminacosmetics.com/ms-pimple-acne-solution-- | Original Acne Facial Wash; matched to official Ms. Pimple Acne Solution Face Wash source page. |
| P024 | Bright Stuff Moisturizer | Emina Official | exact | https://www.eminacosmetics.com/-bright-stuff-moisturizing-cream | Matched to official Bright Stuff Moisturizing Cream page. |
| P025 | Sun Protection Lotion SPF30 | Female Daily Review | exact | https://reviews.femaledaily.com/products/moisturizer/sun-protection-1/emina/sun-protection-spf-30-pa | Matched to Emina Sun Protection SPF30 PA+++ product page. |
| P026 | Moist and Glow Toner | Emina Official | close | https://www.eminacosmetics.com/bright-stuff-face-toner- | Original Moist and Glow Toner; matched to official Bright Stuff Face Toner page. |
| P027 | Acne Spot Gel | Emina Official | exact | https://www.eminacosmetics.com/ms-pimple-acne-solution-spot-gel | Matched to official Ms. Pimple Acne Solution Spot Gel page. |
| P028 | Bright Stuff Serum | Emina Official | exact | https://www.eminacosmetics.com/bright-stuff-serum-30ml | Matched to official Bright Stuff Serum 30ml page. |
| P029 | Niacinamide Toner | Sociolla | exact | https://www.sociolla.com/toner/52497-your-skin-bae-series-toner-niacinamide-7-alpha-arbutin-1-kale | Matched to Avoskin YSB Toner Niacinamide 7% + Alpha Arbutin 1% + Kale page. |
| P030 | Your Skin Bae Serum Niacinamide | Avoskin Official | exact | https://www.avoskinbeauty.com/product/serum-avoskin-your-skin-bae-niacinamide-30-ml-mencerahkan-kulit | Matched to official Avoskin Your Skin Bae Niacinamide serum page. |
| P031 | TIAM Vita B3 Source | TIAM Official | exact | https://tiamglobal.com/products/tiam-vita-b3-source-40ml-1 | Brand in dataset is Avoskin but product is TIAM; source uses official TIAM product page. |
| P032 | Miracle Toner | Avoskin Official | exact | https://www.avoskinbeauty.com/product/toner-avoskin-miraculous-refining-100-ml-aha-bha-pha-eksfoliasi-kulit | Matched to official Avoskin Miraculous Refining Toner page. |
| P033 | Perfect Glow Sunscreen SPF50 | Avoskin Official | close | https://www.avoskinbeauty.com/product-review/sunscreen-avoskin-your-skin-bae-shield-of-sun-spf-50-pa-30-ml | Original Perfect Glow Sunscreen; matched to Avoskin Your Skin Bae Shield of Sun SPF50 PA++++ source page. |
| P034 | Hydrating Facial Wash | Avoskin Official | close | https://www.avoskinbeauty.com/product-category/facial-cleanser | Original Hydrating Facial Wash; matched to Avoskin facial cleanser category showing Natural Sublime Facial Cleanser. |
| P035 | Acne Serum BHA | Avoskin Official | close | https://www.avoskinbeauty.com/product/serum-avoskin-your-skin-bae-salicylic-acid-30-ml-untuk-kulit-komedo | Original Acne Serum BHA; matched to official YSB Salicylic Acid 2% + Zinc serum. |
| P036 | Hydra Bright Serum | Dear Me Beauty Official | close | https://www.dearmebeauty.com/ | Exact Hydra Bright Serum page not found in indexed results; linked to official Dear Me Beauty catalog. |
| P037 | Soothing Toner Centella | Nihonmart | close | https://nihonmart.id/dear-me-beauty-skin-barrier-toner-essence-100ml | Original Soothing Toner Centella; matched to Dear Me Beauty Skin Barrier Toner Essence product source. |
| P038 | Matte Sunscreen SPF50 | Dear Me Beauty Official | exact | https://www.dearmebeauty.com/skincare/231-skin-barrier-sunscreen-gel.html | Matched to official Dear Me Beauty Skin Barrier Sunscreen Gel SPF50 PA++++ page. |
| P039 | Retinol Night Serum | SOCO Review | close | https://review.soco.id/product/face-serum/85773-retinol-blueberry-extract-face-serum | Original Retinol Night Serum; matched to Dear Me Beauty Retinol + Blueberry Extract Face Serum source. |
| P040 | Barrier Repair Moisturizer | Dear Me Beauty Official | exact | https://www.dearmebeauty.com/skincare/241-dear-me-beauty-skin-barrier-water-cream-.html | Matched to official Skin Barrier Water Cream page. |
| P041 | Acne Cleanser BHA | Dear Me Beauty Official | close | https://www.dearmebeauty.com/7-skincare | Exact Acne Cleanser BHA page not found; linked to official skincare catalog showing Skin Barrier Face Gel Cleanser. |
| P042 | Brightening Toner | NPURE Official | exact | https://npureofficial.id/products/npure-licorice-milky-spotlight-toner | Matched to official NPURE Licorice Milky Spotlight Toner page. |
| P043 | Centella Serum | NPURE Official | exact | https://npureofficial.id/products/new-npure-centella-asiatica-power-primer-serum-serum-for-acne-skin-serum-kulit-berjerawat | Matched to official NPURE Centella Asiatica Power Primer Serum page. |
| P044 | Sunscreen SPF50 PA++++ | NPURE Official | exact | https://npureofficial.id/products/cica-beat-the-sun-spf-50-pa | Matched to official NPURE Cica Beat The Sun Glow SPF50 PA++++ page. |
| P045 | Hydrating Cleanser | NPURE Official | close | https://npureofficial.id/collections/centella-asiatica-series | Original Hydrating Cleanser; matched to official Centella series page showing Centella Face Wash. |
| P046 | Moisturizer Centella | NPURE Official | exact | https://npureofficial.id/products/npure-centella-asiatica-acne-clear-barrier-moisturizer | Matched to official NPURE Centella Asiatica Acne Clear Barrier Moisturizer page. |
| P047 | Niacinamide Brightening Serum | Mineral Botanica Official | exact | https://mineralbotanica.com/products/mineral-botanica-niacinamide-serum-with-artichoke-leaf-extract | Matched to official Mineral Botanica Niacinamide Serum with Artichoke Leaf Extract page. |
| P048 | UV Defense Sunscreen SPF50 | Mineral Botanica Official | exact | https://mineralbotanica.com/products/mineral-botanica-sunny-shield-up-sunscreen-spf-50-pa | Matched to official Mineral Botanica Sunny Shield Up Sunscreen SPF50+ PA+++ page. |
| P049 | Hydra Glow Toner | Mineral Botanica Official | close | https://mineralbotanica.com/products/glo-it-up-coq10-hydrating-facial-toner | Original Hydra Glow Toner; matched to official Glo It Up CoQ10 Hydrating Facial Toner page. |
| P050 | Gentle Foam Cleanser | Mineral Botanica Official | close | https://mineralbotanica.com/products/perfect-purifying-facial-foam | Original Gentle Foam Cleanser; matched to official Perfect Purifying Facial Foam page. |
