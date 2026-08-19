import requests

# Staging environment — recommended by OpenFoodFacts docs for testing/development
# so test traffic doesn't hit production or trigger bot protection.
BASE_URL = "https://world.openfoodfacts.net"

# OpenFoodFacts requires a custom User-Agent in the form AppName/Version (ContactEmail)
HEADERS = {
    "User-Agent": "InventoryManagementSystem/1.0 (your-email@example.com)"
}

# Staging requires HTTP Basic Auth with these fixed, publicly documented credentials
# (not a real secret — this is intentional, see OpenFoodFacts API docs)
AUTH = ("off", "off")


def fetch_by_barcode(barcode):
    """Look up a product by barcode. Returns a normalized dict, or None if not found."""
    url = f"{BASE_URL}/api/v2/product/{barcode}.json"
    response = requests.get(url, headers=HEADERS, auth=AUTH, timeout=10)
    response.raise_for_status()
    data = response.json()

    if data.get("status") != 1:
        return None

    return _normalize(data["product"], barcode=barcode)


def fetch_by_name(name, limit=5):
    """Search products by name. Returns a list of normalized dicts (may be empty)."""
    url = f"{BASE_URL}/cgi/search.pl"
    params = {
        "search_terms": name,
        "search_simple": 1,
        "action": "process",
        "json": 1,
        "page_size": limit,
    }
    response = requests.get(url, headers=HEADERS, auth=AUTH, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()

    products = data.get("products", [])
    return [_normalize(p) for p in products]


def _normalize(product, barcode=None):
    """Map OpenFoodFacts' messy field names onto our own item shape."""
    return {
        "name": product.get("product_name") or "Unknown product",
        "barcode": barcode or product.get("code"),
        "brand": product.get("brands"),
        "category": product.get("categories"),
        "image_url": product.get("image_url"),
    }