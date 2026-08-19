# Inventory Management System

A Flask-based REST API for managing e-commerce inventory, with OpenFoodFacts
integration for enriching product data, a CLI client, and full test coverage.

## Features

- CRUD REST API for inventory items
- Product lookup by barcode or name via the OpenFoodFacts API
- CLI tool for interacting with the API without a browser or Postman
- Unit tests for routes, external API calls, and CLI commands

## Project Structure

```
inventory-management-system/
├── app.py                  # Flask app entry point
├── database.py              # In-memory mock database (array of dicts)
├── models.py                 # Item model / data access layer
├── external_api.py           # OpenFoodFacts API integration
├── cli.py                    # CLI frontend
├── routes/
│   ├── __init__.py
│   └── inventory.py          # /inventory route handlers
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_routes.py
│   ├── test_external_api.py
│   └── test_cli.py
├── requirements.txt
└── README.md
```

## Installation & Setup

```bash
# Clone the repo
git clone https://github.com/kirugahdennis/inventory-management-system.git
cd inventory-management-system

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the API server
python app.py
```

The API runs at `http://127.0.0.1:5000` by default.

## API Endpoints

| Method | Endpoint | Description | Body / Params |
|---|---|---|---|
| GET | `/` | Health check | — |
| GET | `/inventory` | List all items | — |
| GET | `/inventory/<id>` | Get a single item | — |
| POST | `/inventory` | Create a new item | `{"name": str, "quantity": int, "price": float, "barcode": str, "brand": str, "category": str}` (only `name` required) |
| PATCH | `/inventory/<id>` | Update fields on an item | any subset of the fields above |
| DELETE | `/inventory/<id>` | Delete an item | — |
| GET | `/inventory/lookup` | Look up a product on OpenFoodFacts | query param `barcode` **or** `name` |

**Example:**
```bash
curl -X POST http://127.0.0.1:5000/inventory \
  -H "Content-Type: application/json" \
  -d '{"name": "Oat Milk", "quantity": 15, "price": 3.99}'
```

## CLI Usage

With the API server running in one terminal, start the CLI in another:

```bash
python cli.py
```

You'll see a menu:

```
--- Inventory CLI ---
1. View all items
2. View item by ID
3. Add new item
4. Update price/stock
5. Delete item
6. Find item on OpenFoodFacts
0. Exit
```

Example — adding an item:

```
Choose an option: 3
Name: Oat Milk
Quantity [0]: 15
Price [0.0]: 3.99
Barcode (optional):
Brand (optional): Oatly
Category (optional): Beverages
Item added:
  [2] Oat Milk | qty: 15 | price: $3.99 | brand: Oatly | barcode: -
```

Example — looking up a product by barcode:

```
Choose an option: 6
Search by (b)arcode or (n)ame? b
Barcode: 3760020508174
  Organic Almond Milk | brand: Silk | barcode: 3760020508174
```

## Running Tests

```bash
pytest -v
```

This runs the full suite: API endpoint tests, mocked OpenFoodFacts API
tests, and CLI command tests (using `unittest.mock` to simulate both the
Flask test client and external HTTP calls).

## Notes

- Storage is an **in-memory array** of dicts (per assignment spec, not a
  persistent database) — data resets on server restart.
- OpenFoodFacts integration uses their **staging environment**
  (`world.openfoodfacts.net`) with the publicly documented `off`/`off`
  Basic Auth credentials, per their API docs, to avoid rate limits and
  bot protection on production.

~Denis Kiarie. 