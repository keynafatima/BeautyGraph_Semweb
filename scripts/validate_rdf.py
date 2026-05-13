r"""
validate_rdf.py

Script validasi RDF untuk project BeautyGraph.

Tujuan:
1. Memastikan file RDF/Turtle bisa dibaca tanpa error.
2. Menghitung total triples.
3. Menghitung jumlah instance beauty:Product.
4. Mengecek apakah jumlah produk sesuai target.
5. Mengecek kelengkapan relasi penting pada setiap produk.

Cara menjalankan dari root project:

    python scripts/validate_rdf.py

Atau dengan path manual:

    python scripts/validate_rdf.py --rdf data/processed/beautygraph.ttl

Jika kamu memakai Python path lengkap di Windows:

    & C:/Users/ASUS/AppData/Local/Programs/Python/Python312/python.exe ./scripts/validate_rdf.py
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable

from rdflib import Graph, Namespace, RDF, URIRef


BEAUTY = Namespace("http://beautygraph.org/ontology#")

DEFAULT_RDF_PATH = Path("data/processed/beautygraph.ttl")
MIN_EXPECTED_TRIPLES = 400
EXPECTED_PRODUCTS = 50


REQUIRED_PRODUCT_PROPERTIES = {
    "productName": BEAUTY.productName,
    "belongsToBrand": BEAUTY.belongsToBrand,
    "belongsToCategory": BEAUTY.belongsToCategory,
    "hasIngredient": BEAUTY.hasIngredient,
    "suitableFor": BEAUTY.suitableFor,
    "targetsConcern": BEAUTY.targetsConcern,
    "hasBenefit": BEAUTY.hasBenefit,
    "hasPriceRange": BEAUTY.hasPriceRange,
    "sourceName": BEAUTY.sourceName,
    "sourceURL": BEAUTY.sourceURL,
}


def print_section(title: str) -> None:
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)


def local_name(uri: URIRef) -> str:
    text = str(uri)
    if "#" in text:
        return text.split("#")[-1]
    return text.rstrip("/").split("/")[-1]


def load_graph(rdf_path: Path) -> Graph:
    if not rdf_path.exists():
        raise FileNotFoundError(
            f"RDF file not found: {rdf_path}\n"
            "Pastikan kamu menjalankan script dari root project BeautyGraph_Semweb, "
            "atau masukkan path RDF secara manual dengan --rdf."
        )

    graph = Graph()
    graph.parse(rdf_path, format="turtle")
    return graph


def get_instances(graph: Graph, rdf_class: URIRef) -> list[URIRef]:
    return sorted(
        {subject for subject in graph.subjects(RDF.type, rdf_class)},
        key=lambda uri: str(uri),
    )


def count_missing_property(graph: Graph, subjects: Iterable[URIRef], prop: URIRef) -> list[URIRef]:
    missing = []
    for subject in subjects:
        if not list(graph.objects(subject, prop)):
            missing.append(subject)
    return missing


def print_basic_summary(graph: Graph) -> None:
    product_count = len(get_instances(graph, BEAUTY.Product))
    brand_count = len(get_instances(graph, BEAUTY.Brand))
    category_count = len(get_instances(graph, BEAUTY.Category))
    ingredient_count = len(get_instances(graph, BEAUTY.Ingredient))
    skin_type_count = len(get_instances(graph, BEAUTY.SkinType))
    concern_count = len(get_instances(graph, BEAUTY.SkinConcern))
    benefit_count = len(get_instances(graph, BEAUTY.Benefit))
    price_range_count = len(get_instances(graph, BEAUTY.PriceRange))

    print_section("BASIC RDF SUMMARY")
    print(f"Total triples      : {len(graph)}")
    print(f"Total products     : {product_count}")
    print(f"Total brands       : {brand_count}")
    print(f"Total categories   : {category_count}")
    print(f"Total ingredients  : {ingredient_count}")
    print(f"Total skin types   : {skin_type_count}")
    print(f"Total concerns     : {concern_count}")
    print(f"Total benefits     : {benefit_count}")
    print(f"Total price ranges : {price_range_count}")


def validate_targets(graph: Graph) -> bool:
    print_section("TARGET VALIDATION")

    total_triples = len(graph)
    product_count = len(get_instances(graph, BEAUTY.Product))

    is_triple_ok = total_triples >= MIN_EXPECTED_TRIPLES
    is_product_ok = product_count == EXPECTED_PRODUCTS

    print(
        f"Triple count >= {MIN_EXPECTED_TRIPLES:<3}: "
        f"{'PASS' if is_triple_ok else 'FAIL'} "
        f"({total_triples} triples)"
    )
    print(
        f"Product count = {EXPECTED_PRODUCTS:<5}: "
        f"{'PASS' if is_product_ok else 'FAIL'} "
        f"({product_count} products)"
    )

    return is_triple_ok and is_product_ok


def validate_required_product_properties(graph: Graph) -> bool:
    print_section("PRODUCT PROPERTY COMPLETENESS")

    products = get_instances(graph, BEAUTY.Product)
    all_ok = True

    for prop_name, prop_uri in REQUIRED_PRODUCT_PROPERTIES.items():
        missing = count_missing_property(graph, products, prop_uri)
        if missing:
            all_ok = False
            print(f"{prop_name:<20}: FAIL ({len(missing)} product(s) missing)")
            sample = ", ".join(local_name(uri) for uri in missing[:5])
            print(f"  Sample missing: {sample}")
        else:
            print(f"{prop_name:<20}: PASS")

    return all_ok


def validate_deprecated_terms(graph: Graph) -> bool:
    print_section("DEPRECATED / TYPO TERM CHECK")

    deprecated_terms = [
        BEAUTY.UnvenSkinTone,
        BEAUTY.DullSkin,
    ]

    all_ok = True

    for term in deprecated_terms:
        found_as_subject = list(graph.triples((term, None, None)))
        found_as_object = list(graph.triples((None, None, term)))
        total_found = len(found_as_subject) + len(found_as_object)

        if total_found > 0:
            all_ok = False
            print(f"{local_name(term):<20}: FAIL ({total_found} triple(s) found)")
        else:
            print(f"{local_name(term):<20}: PASS")

    return all_ok


def run_sample_query(graph: Graph) -> bool:
    print_section("SAMPLE SPARQL QUERY TEST")

    query = """
    PREFIX beauty: <http://beautygraph.org/ontology#>

    SELECT ?product ?name
    WHERE {
        ?product a beauty:Product ;
                 beauty:productName ?name .
    }
    ORDER BY ?product
    LIMIT 10
    """

    try:
        results = list(graph.query(query))
    except Exception as exc:
        print("Sample query: FAIL")
        print(f"Error: {exc}")
        return False

    if not results:
        print("Sample query: FAIL")
        print("Tidak ada produk yang ditemukan.")
        return False

    print("Sample query: PASS")
    print("\nContoh 10 produk pertama:")
    for row in results:
        print(f"- {local_name(row.product)} | {row.name}")

    return True


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate BeautyGraph RDF/Turtle dataset."
    )
    parser.add_argument(
        "--rdf",
        default=str(DEFAULT_RDF_PATH),
        help="Path ke file RDF/Turtle hasil generate. Default: data/processed/beautygraph.ttl",
    )
    args = parser.parse_args()

    rdf_path = Path(args.rdf)

    print_section("BEAUTYGRAPH RDF VALIDATOR")
    print(f"RDF file: {rdf_path}")

    try:
        graph = load_graph(rdf_path)
    except Exception as exc:
        print("\nRDF validation failed.")
        print(f"Error: {exc}")
        raise SystemExit(1)

    print("\nRDF file can be parsed successfully.")

    print_basic_summary(graph)

    target_ok = validate_targets(graph)
    property_ok = validate_required_product_properties(graph)
    deprecated_ok = validate_deprecated_terms(graph)
    query_ok = run_sample_query(graph)

    print_section("FINAL RESULT")

    if target_ok and property_ok and deprecated_ok and query_ok:
        print("RDF VALIDATION SUCCESSFUL")
        print("Dataset RDF BeautyGraph sudah siap lanjut ke tahap SPARQL query.")
    else:
        print("RDF VALIDATION FINISHED WITH WARNINGS/ERRORS")
        print("Periksa bagian FAIL di atas sebelum lanjut ke tahap SPARQL query.")


if __name__ == "__main__":
    main()
