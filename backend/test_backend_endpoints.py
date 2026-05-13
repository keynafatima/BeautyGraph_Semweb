"""
test_backend_endpoints.py

Opsional: script sederhana untuk test endpoint backend.
Pastikan backend sudah berjalan dulu:

    python backend/app.py

Lalu jalankan:

    python backend/test_backend_endpoints.py
"""

from __future__ import annotations

import json
import urllib.parse
import urllib.request


BASE_URL = "http://127.0.0.1:5000"


def get_json(url: str) -> dict:
    with urllib.request.urlopen(url) as response:
        return json.loads(response.read().decode("utf-8"))


def post_json(url: str, payload: dict) -> dict:
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request) as response:
        return json.loads(response.read().decode("utf-8"))


def main() -> None:
    print("Testing /health")
    health = get_json(f"{BASE_URL}/health")
    print(json.dumps(health, indent=2))

    print("\nTesting /filters")
    filters = get_json(f"{BASE_URL}/filters")
    print("success:", filters.get("success"))
    print("filter keys:", list(filters.get("data", {}).keys()))

    print("\nTesting /products?skin_type=OilySkin&concern=Acne")
    products = get_json(f"{BASE_URL}/products?skin_type=OilySkin&concern=Acne&limit=5")
    print("success:", products.get("success"))
    print("rows:", products.get("data", {}).get("count"))

    print("\nTesting POST /sparql")
    query = """
    PREFIX beauty: <http://beautygraph.org/ontology#>
    SELECT ?product ?name
    WHERE {
      ?product a beauty:Product ;
               beauty:productName ?name .
    }
    LIMIT 5
    """
    sparql = post_json(f"{BASE_URL}/sparql", {"query": query})
    print("success:", sparql.get("success"))
    print("rows:", sparql.get("data", {}).get("count"))

    print("\nAll endpoint tests finished.")


if __name__ == "__main__":
    main()
