r"""
test_sparql_queries.py

Script untuk menjalankan semua file .rq di folder queries terhadap RDF BeautyGraph.

Cara menjalankan dari root project:

    python scripts/test_sparql_queries.py

Atau:

    python scripts/test_sparql_queries.py --rdf data/processed/beautygraph.ttl --queries queries
"""

from __future__ import annotations

import argparse
from pathlib import Path
from rdflib import Graph


DEFAULT_RDF_PATH = Path("data/processed/beautygraph.ttl")
DEFAULT_QUERY_DIR = Path("queries")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run BeautyGraph SPARQL query files.")
    parser.add_argument("--rdf", default=str(DEFAULT_RDF_PATH), help="Path RDF/Turtle file.")
    parser.add_argument("--queries", default=str(DEFAULT_QUERY_DIR), help="Folder containing .rq files.")
    parser.add_argument("--limit-print", type=int, default=5, help="Max rows printed per query.")
    args = parser.parse_args()

    rdf_path = Path(args.rdf)
    query_dir = Path(args.queries)

    if not rdf_path.exists():
        raise FileNotFoundError(f"RDF file not found: {rdf_path}")

    if not query_dir.exists():
        raise FileNotFoundError(f"Query folder not found: {query_dir}")

    graph = Graph()
    graph.parse(rdf_path, format="turtle")

    query_files = sorted(query_dir.glob("*.rq"))

    if not query_files:
        raise FileNotFoundError(f"No .rq files found in: {query_dir}")

    print("=" * 72)
    print("BEAUTYGRAPH SPARQL QUERY TEST")
    print("=" * 72)
    print(f"RDF file     : {rdf_path}")
    print(f"Total triples: {len(graph)}")
    print(f"Query folder : {query_dir}")
    print(f"Total queries: {len(query_files)}")

    all_ok = True

    for query_file in query_files:
        print("\n" + "-" * 72)
        print(f"Running: {query_file.name}")
        print("-" * 72)

        query_text = query_file.read_text(encoding="utf-8")

        try:
            rows = list(graph.query(query_text))
            print(f"Status: PASS")
            print(f"Rows  : {len(rows)}")

            for idx, row in enumerate(rows[: args.limit_print], start=1):
                row_values = [str(value) for value in row]
                print(f"{idx}. " + " | ".join(row_values))

            if len(rows) > args.limit_print:
                print(f"... {len(rows) - args.limit_print} more row(s)")

        except Exception as exc:
            all_ok = False
            print("Status: FAIL")
            print(f"Error : {exc}")

    print("\n" + "=" * 72)
    if all_ok:
        print("ALL QUERIES PASSED")
    else:
        print("SOME QUERIES FAILED")
    print("=" * 72)


if __name__ == "__main__":
    main()
