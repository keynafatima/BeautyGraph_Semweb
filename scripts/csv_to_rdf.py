"""
csv_to_rdf.py

Convert BeautyGraph product CSV data into an RDF/Turtle knowledge graph.

Input:
  - data/raw/beautygraph_50products_sourced.csv
  - data/ontology/beautygraph_ontology_clean.ttl

Output:
  - data/processed/beautygraph.ttl

How to run from project root:
  python scripts/csv_to_rdf.py

Or run with custom paths:
  python scripts/csv_to_rdf.py \
    --csv data/raw/beautygraph_50products_sourced.csv \
    --ontology data/ontology/beautygraph_ontology_clean.ttl \
    --output data/processed/beautygraph.ttl
"""

from __future__ import annotations

import argparse
import math
import re
from pathlib import Path
from typing import Iterable, List, Optional

import pandas as pd
from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import OWL, RDF, RDFS, XSD


BEAUTY = Namespace("http://beautygraph.org/ontology#")


# Some labels need stable URI names that already exist in the ontology file.
# Any item not listed here will be converted automatically into a safe CamelCase URI.
URI_OVERRIDES = {
    # Brand
    "Dear Me Beauty": "DearMeBeauty",
    "NPURE": "Npure",
    "Npure": "Npure",
    "Mineral Botanica": "MineralBotanica",

    # Common ontology terms
    "All Skin Types": "AllSkinTypes",
    "AllSkinTypes": "AllSkinTypes",
    "Acne-Prone Skin": "AcneProneSkin",
    "AcneProneSkin": "AcneProneSkin",
    "Oily Skin": "OilySkin",
    "OilySkin": "OilySkin",
    "Dry Skin": "DrySkin",
    "DrySkin": "DrySkin",
    "Normal Skin": "NormalSkin",
    "NormalSkin": "NormalSkin",
    "Combination Skin": "CombinationSkin",
    "CombinationSkin": "CombinationSkin",
    "Sensitive Skin": "SensitiveSkin",
    "SensitiveSkin": "SensitiveSkin",

    # Concern / benefit edge cases
    "Uneven Skin Tone": "UnevenSkinTone",
    "UnevenSkinTone": "UnevenSkinTone",
    "Fine Lines": "FineLine",
    "FineLine": "FineLine",
    "Large Pores": "LargePores",
    "LargePores": "LargePores",
    "Acne Marks": "AcneMarks",
    "AcneMarks": "AcneMarks",
    "Sun Damage": "SunDamage",
    "SunDamage": "SunDamage",
    "Pore Care": "PoreCare",
    "PoreCare": "PoreCare",
    "Even Skin Tone": "EvenSkinTone",
    "EvenSkinTone": "EvenSkinTone",
    "Sun Protection": "SunProtection",
    "SunProtection": "SunProtection",
    "Barrier Repair": "BarrierRepair",
    "BarrierRepair": "BarrierRepair",
    "Mattifying Effect": "MattifyingEffect",
    "MattifyingEffect": "MattifyingEffect",
    "Acne Treatment": "AcneTreatment",
    "AcneTreatment": "AcneTreatment",
    "Anti-Aging": "AntiAging",
    "AntiAging": "AntiAging",
}


REQUIRED_COLUMNS = [
    "product_id",
    "product_name",
    "brand",
    "category",
    "skin_type",
    "price_range",
]

INGREDIENT_COLUMNS = ["ingredient_1", "ingredient_2", "ingredient_3", "ingredient_4", "ingredient_5"]
CONCERN_COLUMNS = ["concern_1", "concern_2"]
BENEFIT_COLUMNS = ["benefit_1", "benefit_2"]


class BeautyGraphConversionError(Exception):
    """Raised when the BeautyGraph CSV cannot be converted safely."""


def is_blank(value: object) -> bool:
    """Return True when a CSV cell should be treated as empty."""
    if value is None:
        return True
    if isinstance(value, float) and math.isnan(value):
        return True
    text = str(value).strip()
    return text == "" or text.lower() in {"nan", "none", "null"}


def clean_text(value: object) -> str:
    """Normalize a CSV value into a clean string."""
    if is_blank(value):
        return ""
    return re.sub(r"\s+", " ", str(value).strip())


def split_multivalue(value: object) -> List[str]:
    """
    Split multi-value cells.

    The dataset primarily uses pipe-separated values, e.g.:
      OilySkin|CombinationSkin|SensitiveSkin

    This function also tolerates semicolons, commas, and newlines.
    """
    text = clean_text(value)
    if not text:
        return []
    parts = re.split(r"\s*[|;,\n]\s*", text)
    return [part.strip() for part in parts if part.strip()]


def to_camel_uri_name(label: str) -> str:
    """Convert a human-readable label into a safe BeautyGraph URI local name."""
    label = clean_text(label)
    if not label:
        raise ValueError("Cannot create URI for blank label.")
    if label in URI_OVERRIDES:
        return URI_OVERRIDES[label]

    # Preserve already-CamelCase identifiers such as OilySkin or AcneMarks.
    if re.fullmatch(r"[A-Za-z][A-Za-z0-9]*", label):
        return label

    # Remove characters that cannot safely appear in URI local names and CamelCase words.
    words = re.findall(r"[A-Za-z0-9]+", label)
    if not words:
        raise ValueError(f"Cannot create URI from label: {label!r}")

    return "".join(word[:1].upper() + word[1:] for word in words)


def pretty_label(identifier_or_label: str) -> str:
    """Create a readable rdfs:label from a CamelCase identifier or original label."""
    text = clean_text(identifier_or_label)
    if not text:
        return ""

    # If text already has spaces or hyphens, keep it readable with normalized spacing.
    if " " in text or "-" in text:
        return text

    # Convert CamelCase into separate words.
    text = re.sub(r"(?<=[a-z])(?=[A-Z])", " ", text)
    text = re.sub(r"(?<=[A-Z])(?=[A-Z][a-z])", " ", text)
    return text.strip()


def beauty_uri(label_or_id: str) -> URIRef:
    """Return a BeautyGraph URIRef for a label or existing identifier."""
    return BEAUTY[to_camel_uri_name(label_or_id)]


def validate_columns(df: pd.DataFrame) -> None:
    """Ensure the CSV contains all columns needed for conversion."""
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    missing += [col for col in INGREDIENT_COLUMNS if col not in df.columns]
    missing += [col for col in CONCERN_COLUMNS if col not in df.columns]
    missing += [col for col in BENEFIT_COLUMNS if col not in df.columns]

    if missing:
        raise BeautyGraphConversionError(
            "CSV is missing required columns: " + ", ".join(sorted(set(missing)))
        )


def add_named_individual(
    graph: Graph,
    uri: URIRef,
    class_uri: URIRef,
    label: str,
    datatype_property: Optional[URIRef] = None,
) -> None:
    """
    Add a reusable individual such as Brand, Ingredient, SkinType, or Benefit.

    RDFLib automatically ignores exact duplicate triples, so it is safe to call this
    repeatedly while looping over product rows.
    """
    readable = pretty_label(label)
    graph.add((uri, RDF.type, class_uri))
    graph.add((uri, RDFS.label, Literal(readable, datatype=XSD.string)))
    if datatype_property is not None:
        graph.add((uri, datatype_property, Literal(readable, datatype=XSD.string)))


def add_relation_list(
    graph: Graph,
    product_uri: URIRef,
    values: Iterable[str],
    predicate: URIRef,
    target_class: URIRef,
    datatype_property: Optional[URIRef] = None,
) -> int:
    """Add relation triples from one product to a list of target individuals."""
    count = 0
    seen = set()
    for value in values:
        value = clean_text(value)
        if not value:
            continue
        target_uri = beauty_uri(value)
        if target_uri in seen:
            continue
        seen.add(target_uri)

        add_named_individual(graph, target_uri, target_class, value, datatype_property)
        graph.add((product_uri, predicate, target_uri))
        count += 1
    return count


def collect_columns(row: pd.Series, columns: Iterable[str]) -> List[str]:
    """Collect and split values from several CSV columns."""
    values: List[str] = []
    for col in columns:
        values.extend(split_multivalue(row.get(col, "")))
    return values


def convert_csv_to_rdf(csv_path: Path, ontology_path: Path, output_path: Path) -> Graph:
    """Load ontology + CSV and serialize the complete BeautyGraph RDF dataset."""
    csv_path = Path(csv_path)
    ontology_path = Path(ontology_path)
    output_path = Path(output_path)

    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")
    if not ontology_path.exists():
        raise FileNotFoundError(f"Ontology file not found: {ontology_path}")

    df = pd.read_csv(csv_path)
    validate_columns(df)

    graph = Graph()
    graph.bind("beauty", BEAUTY)
    graph.bind("rdf", RDF)
    graph.bind("rdfs", RDFS)
    graph.bind("owl", OWL)
    graph.bind("xsd", XSD)

    # Load the base ontology first, then add product instances from CSV.
    graph.parse(str(ontology_path), format="turtle")

    product_ids = set()
    for idx, row in df.iterrows():
        product_id = clean_text(row.get("product_id"))
        product_name = clean_text(row.get("product_name"))
        brand = clean_text(row.get("brand"))
        category = clean_text(row.get("category"))
        price_range = clean_text(row.get("price_range"))
        source_name = clean_text(row.get("source_name"))
        source_url = clean_text(row.get("source_url"))

        if not product_id:
            raise BeautyGraphConversionError(f"Row {idx + 2}: product_id is blank.")
        if product_id in product_ids:
            raise BeautyGraphConversionError(f"Duplicate product_id found: {product_id}")
        product_ids.add(product_id)

        if not product_name:
            raise BeautyGraphConversionError(f"Row {idx + 2} ({product_id}): product_name is blank.")
        if not brand:
            raise BeautyGraphConversionError(f"Row {idx + 2} ({product_id}): brand is blank.")
        if not category:
            raise BeautyGraphConversionError(f"Row {idx + 2} ({product_id}): category is blank.")
        if not price_range:
            raise BeautyGraphConversionError(f"Row {idx + 2} ({product_id}): price_range is blank.")

        product_uri = BEAUTY[product_id]

        # Product identity and labels.
        graph.add((product_uri, RDF.type, BEAUTY.Product))
        graph.add((product_uri, RDFS.label, Literal(product_name, datatype=XSD.string)))
        graph.add((product_uri, BEAUTY.productName, Literal(product_name, datatype=XSD.string)))

        # Source metadata.
        if source_name:
            graph.add((product_uri, BEAUTY.sourceName, Literal(source_name, datatype=XSD.string)))
        if source_url:
            graph.add((product_uri, BEAUTY.sourceURL, Literal(source_url, datatype=XSD.anyURI)))

        # Brand, category, and price range.
        add_relation_list(
            graph,
            product_uri,
            [brand],
            BEAUTY.belongsToBrand,
            BEAUTY.Brand,
            BEAUTY.brandName,
        )
        add_relation_list(
            graph,
            product_uri,
            [category],
            BEAUTY.belongsToCategory,
            BEAUTY.Category,
        )
        add_relation_list(
            graph,
            product_uri,
            [price_range],
            BEAUTY.hasPriceRange,
            BEAUTY.PriceRange,
        )

        # Multi-value relations.
        ingredients = collect_columns(row, INGREDIENT_COLUMNS)
        skin_types = collect_columns(row, ["skin_type"])
        concerns = collect_columns(row, CONCERN_COLUMNS)
        benefits = collect_columns(row, BENEFIT_COLUMNS)

        add_relation_list(
            graph,
            product_uri,
            ingredients,
            BEAUTY.hasIngredient,
            BEAUTY.Ingredient,
            BEAUTY.ingredientName,
        )
        add_relation_list(
            graph,
            product_uri,
            skin_types,
            BEAUTY.suitableFor,
            BEAUTY.SkinType,
        )
        add_relation_list(
            graph,
            product_uri,
            concerns,
            BEAUTY.targetsConcern,
            BEAUTY.SkinConcern,
        )
        add_relation_list(
            graph,
            product_uri,
            benefits,
            BEAUTY.hasBenefit,
            BEAUTY.Benefit,
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    graph.serialize(destination=str(output_path), format="turtle")
    return graph


def count_products(graph: Graph) -> int:
    """Count Product individuals in the graph."""
    return sum(1 for _ in graph.subjects(RDF.type, BEAUTY.Product))


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Convert BeautyGraph CSV data into RDF/Turtle.")
    parser.add_argument(
        "--csv",
        default="data/raw/beautygraph_50products_sourced.csv",
        help="Path to sourced product CSV.",
    )
    parser.add_argument(
        "--ontology",
        default="data/ontology/beautygraph_ontology_clean.ttl",
        help="Path to base ontology TTL.",
    )
    parser.add_argument(
        "--output",
        default="data/processed/beautygraph.ttl",
        help="Output path for generated RDF/Turtle file.",
    )
    return parser


def main() -> None:
    parser = build_arg_parser()
    args = parser.parse_args()

    graph = convert_csv_to_rdf(
        csv_path=Path(args.csv),
        ontology_path=Path(args.ontology),
        output_path=Path(args.output),
    )

    print("BeautyGraph RDF conversion finished.")
    print(f"Output file   : {args.output}")
    print(f"Total triples : {len(graph)}")
    print(f"Total products: {count_products(graph)}")


if __name__ == "__main__":
    main()
