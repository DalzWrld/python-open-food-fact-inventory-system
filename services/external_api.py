"""
Handles all communication with the OpenFoodFacts API.

Two lookup methods are supported:
    - fetch_by_barcode(barcode): exact product lookup
    - fetch_by_name(name): keyword search, returns the best match

Both functions return a small, normalized dict (or None if nothing was
found / the request failed), so the rest of the app never has to deal
with OpenFoodFacts' raw response shape directly.
"""

import requests

BARCODE_URL = "https://world.openfoodfacts.org/api/v2/product/{barcode}.json"
SEARCH_URL = "https://world.openfoodfacts.org/cgi/search.pl"

REQUEST_TIMEOUT = 10  # seconds


def _normalize_product(product):
    """Pull out just the fields we care about from an OpenFoodFacts product."""
    return {
        "name": product.get("product_name") or "Unknown product",
        "brand": product.get("brands", ""),
        "barcode": product.get("code", ""),
        "ingredients": product.get("ingredients_text", ""),
        "source": "openfoodfacts",
    }


def fetch_by_barcode(barcode):
    """
    Look up a single product by its barcode.
    Returns a normalized product dict, or None if not found / on error.
    """
    try:
        response = requests.get(
            BARCODE_URL.format(barcode=barcode), timeout=REQUEST_TIMEOUT
        )
        response.raise_for_status()
    except requests.RequestException:
        return None

    data = response.json()

    if data.get("status") != 1:
        return None

    return _normalize_product(data.get("product", {}))


def fetch_by_name(name):
    """
    Search for a product by name/keyword. Returns the first matching
    result as a normalized product dict, or None if nothing was found
    / on error.
    """
    params = {
        "search_terms": name,
        "search_simple": 1,
        "action": "process",
        "json": 1,
        "page_size": 1,
    }

    try:
        response = requests.get(SEARCH_URL, params=params, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
    except requests.RequestException:
        return None

    data = response.json()
    products = data.get("products", [])

    if not products:
        return None

    return _normalize_product(products[0])
