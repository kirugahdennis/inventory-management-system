
from flask import Blueprint, request, jsonify
from models import Item
import external_api

inventory_bp = Blueprint("inventory", __name__, url_prefix="/inventory")


@inventory_bp.route("", methods=["GET"])
def get_all_items():
    items = Item.find_all()
    return jsonify([i.to_dict() for i in items]), 200


@inventory_bp.route("/<int:item_id>", methods=["GET"])
def get_item(item_id):
    item = Item.find_by_id(item_id)
    if item is None:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(item.to_dict()), 200


@inventory_bp.route("", methods=["POST"])
def create_item():
    data = request.get_json(silent=True)
    if not data or not data.get("name"):
        return jsonify({"error": "Field 'name' is required"}), 400

    item = Item.create(
        name=data["name"],
        barcode=data.get("barcode"),
        quantity=data.get("quantity", 0),
        price=data.get("price", 0.0),
        category=data.get("category"),
        brand=data.get("brand"),
        image_url=data.get("image_url"),
        ingredients_text=data.get("ingredients_text"),
    )
    return jsonify(item.to_dict()), 201


@inventory_bp.route("/<int:item_id>", methods=["PATCH"])
def update_item(item_id):
    item = Item.find_by_id(item_id)
    if item is None:
        return jsonify({"error": "Item not found"}), 404

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "No update fields provided"}), 400

    item.update(**data)
    return jsonify(item.to_dict()), 200


@inventory_bp.route("/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    item = Item.find_by_id(item_id)
    if item is None:
        return jsonify({"error": "Item not found"}), 404

    item.delete()
    return "", 204


@inventory_bp.route("/lookup", methods=["GET"])
def lookup_external():
    barcode = request.args.get("barcode")
    name = request.args.get("name")

    if not barcode and not name:
        return jsonify({"error": "Provide a 'barcode' or 'name' query param"}), 400

    try:
        if barcode:
            result = external_api.fetch_by_barcode(barcode)
            if result is None:
                return jsonify({"error": "Product not found"}), 404
            return jsonify(result), 200
        else:
            results = external_api.fetch_by_name(name)
            return jsonify(results), 200
    except Exception as e:
        return jsonify({"error": f"External API error: {str(e)}"}), 502