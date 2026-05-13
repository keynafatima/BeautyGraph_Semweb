"""
BeautyGraph Flask SPARQL Endpoint

Endpoint:
- GET  /health
- GET  /sparql?query=...
- POST /sparql
- GET  /products
- GET  /filters

Cara menjalankan dari root project:

    pip install -r backend/requirements.txt
    python backend/app.py

Default RDF path:
    data/processed/beautygraph.ttl

Bisa override dengan environment variable:
    BEAUTYGRAPH_RDF_PATH=data/processed/beautygraph.ttl
"""

from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Any

from flask import Flask, jsonify, request
from flask_cors import CORS
from rdflib import Graph, Literal, Namespace, RDF, URIRef
from rdflib.query import ResultRow


BEAUTY = Namespace("http://beautygraph.org/ontology#")

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RDF_PATH = PROJECT_ROOT / "data" / "processed" / "beautygraph.ttl"
RDF_PATH = Path(os.getenv("BEAUTYGRAPH_RDF_PATH", str(DEFAULT_RDF_PATH)))

app = Flask(__name__)
CORS(app)

graph = Graph()


# ---------------------------------------------------------------------------
# Utility functions
# ---------------------------------------------------------------------------

def load_rdf() -> None:
    """Load RDF/Turtle dataset into global graph."""
    global graph

    if not RDF_PATH.exists():
        raise FileNotFoundError(
            f"RDF file not found: {RDF_PATH}. "
            "Pastikan file data/processed/beautygraph.ttl sudah dibuat."
        )

    graph = Graph()
    graph.parse(RDF_PATH, format="turtle")


def local_name(value: Any) -> str:
    """Return readable local name from URIRef."""
    text = str(value)
    if "#" in text:
        return text.split("#")[-1]
    return text.rstrip("/").split("/")[-1]


def humanize_identifier(value: str) -> str:
    """
    Convert identifier into readable label.
    Example:
    - OilySkin -> Oily Skin
    - HyaluronicAcid -> Hyaluronic Acid
    """
    if not value:
        return value
    value = value.replace("_", " ").replace("-", " ")
    value = re.sub(r"([a-z])([A-Z])", r"\1 \2", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value


def node_to_json(value: Any) -> dict[str, Any]:
    """Serialize RDF node into JSON-friendly object."""
    if isinstance(value, URIRef):
        name = local_name(value)
        return {
            "type": "uri",
            "value": str(value),
            "localName": name,
            "label": humanize_identifier(name),
        }

    if isinstance(value, Literal):
        return {
            "type": "literal",
            "value": str(value),
            "datatype": str(value.datatype) if value.datatype else None,
            "language": value.language,
        }

    return {
        "type": type(value).__name__,
        "value": str(value),
    }


def query_results_to_json(results: Any) -> dict[str, Any]:
    """Convert SPARQL SELECT/ASK/CONSTRUCT/DESCRIBE result into JSON."""
    result_type = getattr(results, "type", None)

    if result_type == "ASK":
        return {
            "type": "ASK",
            "boolean": bool(results.askAnswer),
        }

    if result_type in {"CONSTRUCT", "DESCRIBE"}:
        result_graph = Graph()
        for triple in results:
            result_graph.add(triple)

        turtle = result_graph.serialize(format="turtle")
        return {
            "type": result_type,
            "tripleCount": len(result_graph),
            "turtle": turtle,
        }

    variables = [str(var) for var in results.vars]
    rows = []

    for row in results:
        row_dict = {}
        for var in results.vars:
            value = row.get(var)
            row_dict[str(var)] = node_to_json(value) if value is not None else None
        rows.append(row_dict)

    return {
        "type": "SELECT",
        "variables": variables,
        "count": len(rows),
        "results": rows,
    }


def run_sparql(query_text: str) -> dict[str, Any]:
    """Run SPARQL query and return JSON-friendly result."""
    if not query_text or not query_text.strip():
        raise ValueError("Query tidak boleh kosong.")

    results = graph.query(query_text)
    return query_results_to_json(results)


def make_values_query(rdf_class: URIRef) -> str:
    """Build SPARQL query for a class value list."""
    class_name = local_name(rdf_class)

    return f"""
    PREFIX beauty: <http://beautygraph.org/ontology#>

    SELECT DISTINCT ?uri ?id ?label
    WHERE {{
      ?uri a beauty:{class_name} .
      BIND(STRAFTER(STR(?uri), "#") AS ?id)
      BIND(REPLACE(STRAFTER(STR(?uri), "#"), "([a-z])([A-Z])", "$1 $2") AS ?label)
    }}
    ORDER BY ?label
    """


def read_values(rdf_class: URIRef) -> list[dict[str, str]]:
    """Return all individuals of a class as filter options."""
    results = graph.query(make_values_query(rdf_class))

    values = []
    for row in results:
        values.append(
            {
                "uri": str(row.uri),
                "id": str(row.id),
                "label": str(row.label),
            }
        )

    return values


def validate_identifier(value: str | None) -> str | None:
    """
    Validate identifier used in /products filter.
    Only allows safe local names such as OilySkin, Niacinamide, P001.
    """
    if value is None or value == "":
        return None

    if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", value):
        raise ValueError(f"Invalid identifier: {value}")

    return value


def build_products_query(filters: dict[str, str | None], limit: int) -> str:
    """
    Build product search query from query params.
    Supported filters:
    - skin_type
    - concern
    - ingredient
    - brand
    - category
    - benefit
    - price_range
    """
    patterns = [
        "?product a beauty:Product ;",
        "         beauty:productName ?productName ;",
        "         beauty:belongsToBrand ?brand ;",
        "         beauty:belongsToCategory ?category ;",
        "         beauty:hasPriceRange ?priceRange ;",
        "         beauty:sourceURL ?sourceURL .",
    ]

    if filters.get("skin_type"):
        patterns.append(f"?product beauty:suitableFor beauty:{filters['skin_type']} .")
    if filters.get("concern"):
        patterns.append(f"?product beauty:targetsConcern beauty:{filters['concern']} .")
    if filters.get("ingredient"):
        patterns.append(f"?product beauty:hasIngredient beauty:{filters['ingredient']} .")
    if filters.get("brand"):
        patterns.append(f"?product beauty:belongsToBrand beauty:{filters['brand']} .")
    if filters.get("category"):
        patterns.append(f"?product beauty:belongsToCategory beauty:{filters['category']} .")
    if filters.get("benefit"):
        patterns.append(f"?product beauty:hasBenefit beauty:{filters['benefit']} .")
    if filters.get("price_range"):
        patterns.append(f"?product beauty:hasPriceRange beauty:{filters['price_range']} .")

    where_body = "\n      ".join(patterns)

    return f"""
    PREFIX beauty: <http://beautygraph.org/ontology#>

    SELECT DISTINCT ?product ?productName ?brandName ?categoryName ?priceRangeName ?sourceURL
    WHERE {{
      {where_body}

      BIND(REPLACE(STRAFTER(STR(?brand), "#"), "([a-z])([A-Z])", "$1 $2") AS ?brandName)
      BIND(STRAFTER(STR(?category), "#") AS ?categoryName)
      BIND(STRAFTER(STR(?priceRange), "#") AS ?priceRangeName)
    }}
    ORDER BY ?brandName ?productName
    LIMIT {limit}
    """


def get_product_count() -> int:
    return len({s for s in graph.subjects(RDF.type, BEAUTY.Product)})


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.get("/")
def index():
    return jsonify(
        {
            "app": "BeautyGraph SPARQL Endpoint",
            "message": "Backend is running.",
            "endpoints": {
                "health": "GET /health",
                "sparql_get": "GET /sparql?query=...",
                "sparql_post": "POST /sparql",
                "products": "GET /products",
                "filters": "GET /filters",
            },
        }
    )


@app.get("/health")
def health():
    return jsonify(
        {
            "status": "ok",
            "rdfPath": str(RDF_PATH),
            "totalTriples": len(graph),
            "totalProducts": get_product_count(),
        }
    )


@app.get("/sparql")
def sparql_get():
    query_text = request.args.get("query", "")

    try:
        data = run_sparql(query_text)
        return jsonify({"success": True, "data": data})
    except Exception as exc:
        return jsonify({"success": False, "error": str(exc)}), 400


@app.post("/sparql")
def sparql_post():
    payload = request.get_json(silent=True) or {}

    query_text = (
        payload.get("query")
        or request.form.get("query")
        or request.data.decode("utf-8", errors="ignore")
    )

    try:
        data = run_sparql(query_text)
        return jsonify({"success": True, "data": data})
    except Exception as exc:
        return jsonify({"success": False, "error": str(exc)}), 400


@app.get("/products")
def products():
    try:
        limit = int(request.args.get("limit", 50))
        limit = max(1, min(limit, 200))

        filters = {
            "skin_type": validate_identifier(request.args.get("skin_type")),
            "concern": validate_identifier(request.args.get("concern")),
            "ingredient": validate_identifier(request.args.get("ingredient")),
            "brand": validate_identifier(request.args.get("brand")),
            "category": validate_identifier(request.args.get("category")),
            "benefit": validate_identifier(request.args.get("benefit")),
            "price_range": validate_identifier(request.args.get("price_range")),
        }

        query_text = build_products_query(filters, limit)
        data = run_sparql(query_text)

        return jsonify(
            {
                "success": True,
                "filters": {key: value for key, value in filters.items() if value},
                "data": data,
            }
        )

    except Exception as exc:
        return jsonify({"success": False, "error": str(exc)}), 400


@app.get("/filters")
def filters():
    try:
        data = {
            "brands": read_values(BEAUTY.Brand),
            "categories": read_values(BEAUTY.Category),
            "ingredients": read_values(BEAUTY.Ingredient),
            "skinTypes": read_values(BEAUTY.SkinType),
            "concerns": read_values(BEAUTY.SkinConcern),
            "benefits": read_values(BEAUTY.Benefit),
            "priceRanges": read_values(BEAUTY.PriceRange),
        }

        return jsonify({"success": True, "data": data})

    except Exception as exc:
        return jsonify({"success": False, "error": str(exc)}), 400


# ---------------------------------------------------------------------------
# App entrypoint
# ---------------------------------------------------------------------------

try:
    load_rdf()
except Exception as startup_error:
    print("=" * 72)
    print("BEAUTYGRAPH BACKEND STARTUP ERROR")
    print("=" * 72)
    print(startup_error)
    print("=" * 72)
    raise


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
