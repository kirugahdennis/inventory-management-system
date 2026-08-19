
"""In-memory mock database — a list of dicts standing in for a real DB,
per assignment spec. Data resets each time the app restarts."""

_next_id = 1

# Seed data shaped like what OpenFoodFacts might return
items = [
    {
        "id": 1,
        "name": "Organic Almond Milk",
        "barcode": "3760020508174",
        "quantity": 25,
        "price": 3.49,
        "category": "Beverages",
        "brand": "Silk",
        "ingredients_text": "Filtered water, almonds, cane sugar",
        "image_url": None,
    },
]
_next_id = 2  # next id to assign


def get_next_id():
    global _next_id
    current = _next_id
    _next_id += 1
    return current