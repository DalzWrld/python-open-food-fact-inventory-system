import requests

BARCODE_URL = "https://world.openfoodfacts.org/api/v2/product/{barcode}.json"
SEARCH_URL = "https://world.openfoodfacts.org/cgi/search.pl"

REQUEST_TIMEOUT = 10


def _normalize_product(product):
    return {
        "product_name": product.get("product_name") or "Unknown product",
        "brands": product.get("brands", ""),
        "barcode": product.get("code", ""),
        "ingredients_text": product.get("ingredients_text", ""),
        "source": "openfoodfacts",
    }


def fetch_by_barcode(barcode):
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


def fetch_by_name(name, limit=5):
    params = {
        "search_terms": name,
        "search_simple": 1,
        "action": "process",
        "json": 1,
        "page_size": limit,
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

    return [_normalize_product(p) for p in products]
