
"""CLI frontend for the Inventory Management API."""
import requests

BASE_URL = "http://127.0.0.1:5000/inventory"


def _print_item(item):
    print(f"  [{item['id']}] {item['name']}"
          f" | qty: {item['quantity']} | price: ${item['price']:.2f}"
          f" | brand: {item.get('brand') or '-'}"
          f" | barcode: {item.get('barcode') or '-'}")


def view_all():
    try:
        resp = requests.get(BASE_URL, timeout=10)
        resp.raise_for_status()
        items = resp.json()
        if not items:
            print("No items in inventory.")
            return
        for item in items:
            _print_item(item)
    except requests.RequestException as e:
        print(f"Error contacting API: {e}")


def view_one():
    item_id = input("Item ID: ").strip()
    try:
        resp = requests.get(f"{BASE_URL}/{item_id}", timeout=10)
        if resp.status_code == 404:
            print("Item not found.")
            return
        resp.raise_for_status()
        _print_item(resp.json())
    except ValueError:
        print("Item ID must be a number.")
    except requests.RequestException as e:
        print(f"Error contacting API: {e}")


def add_item():
    name = input("Name: ").strip()
    if not name:
        print("Name is required.")
        return
    try:
        quantity = int(input("Quantity [0]: ") or 0)
        price = float(input("Price [0.0]: ") or 0.0)
    except ValueError:
        print("Quantity must be an integer and price must be a number.")
        return

    barcode = input("Barcode (optional): ").strip() or None
    brand = input("Brand (optional): ").strip() or None
    category = input("Category (optional): ").strip() or None

    payload = {
        "name": name, "quantity": quantity, "price": price,
        "barcode": barcode, "brand": brand, "category": category,
    }
    try:
        resp = requests.post(BASE_URL, json=payload, timeout=10)
        resp.raise_for_status()
        print("Item added:")
        _print_item(resp.json())
    except requests.RequestException as e:
        print(f"Error contacting API: {e}")


def update_item():
    item_id = input("Item ID to update: ").strip()
    print("Leave blank to skip a field.")
    fields = {}

    price = input("New price: ").strip()
    if price:
        try:
            fields["price"] = float(price)
        except ValueError:
            print("Invalid price, skipping.")

    qty = input("New quantity: ").strip()
    if qty:
        try:
            fields["quantity"] = int(qty)
        except ValueError:
            print("Invalid quantity, skipping.")

    if not fields:
        print("Nothing to update.")
        return

    try:
        resp = requests.patch(f"{BASE_URL}/{item_id}", json=fields, timeout=10)
        if resp.status_code == 404:
            print("Item not found.")
            return
        resp.raise_for_status()
        print("Item updated:")
        _print_item(resp.json())
    except requests.RequestException as e:
        print(f"Error contacting API: {e}")


def delete_item():
    item_id = input("Item ID to delete: ").strip()
    try:
        resp = requests.delete(f"{BASE_URL}/{item_id}", timeout=10)
        if resp.status_code == 404:
            print("Item not found.")
            return
        resp.raise_for_status()
        print("Item deleted.")
    except requests.RequestException as e:
        print(f"Error contacting API: {e}")


def find_on_api():
    mode = input("Search by (b)arcode or (n)ame? ").strip().lower()
    params = {}
    if mode == "b":
        params["barcode"] = input("Barcode: ").strip()
    elif mode == "n":
        params["name"] = input("Product name: ").strip()
    else:
        print("Invalid choice.")
        return

    try:
        resp = requests.get(f"{BASE_URL}/lookup", params=params, timeout=15)
        if resp.status_code == 404:
            print("Product not found.")
            return
        resp.raise_for_status()
        data = resp.json()
        results = data if isinstance(data, list) else [data]
        for r in results:
            print(f"  {r.get('name')} | brand: {r.get('brand') or '-'}"
                  f" | barcode: {r.get('barcode') or '-'}")
    except requests.RequestException as e:
        print(f"Error contacting external API: {e}")


MENU = {
    "1": ("View all items", view_all),
    "2": ("View item by ID", view_one),
    "3": ("Add new item", add_item),
    "4": ("Update price/stock", update_item),
    "5": ("Delete item", delete_item),
    "6": ("Find item on OpenFoodFacts", find_on_api),
    "0": ("Exit", None),
}


def main():
    while True:
        print("\n--- Inventory CLI ---")
        for key, (label, _) in MENU.items():
            print(f"{key}. {label}")
        choice = input("Choose an option: ").strip()

        if choice == "0":
            print("Goodbye.")