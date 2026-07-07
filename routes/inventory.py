from flask import Blueprint, jsonify, request

from data import store
from services import external_api

inventory_bp = Blueprint("inventory", __name__, url_prefix="/api/inventory")


def _success(data, status_code=200):
    return jsonify({"status": "success", "data": data}), status_code


def _error(message, status_code=404):
    return jsonify({"status": "error", "message": message}), status_code


@inventory_bp.route("", methods=["GET"])
def get_all_items():
    return _success(store.get_all_items())


@inventory_bp.route("/<int:item_id>", methods=["GET"])
def get_item(item_id):
    item = store.get_item_by_id(item_id)
    if item is None:
        return _error(f"Item with id {item_id} not found")
    return _success(item)


@inventory_bp.route("", methods=["POST"])
def create_item():
    data = request.get_json(silent=True)
    if not data or "product_name" not in data:
        return _error("Request body must include at least a 'product_name' field", 400)

    new_item = store.add_item(data)
    return _success(new_item, 201)


@inventory_bp.route("/<int:item_id>", methods=["PATCH"])
def update_item(item_id):
    data = request.get_json(silent=True)
    if not data:
        return _error("Request body must contain JSON fields to update", 400)

    updated_item = store.update_item(item_id, data)
    if updated_item is None:
        return _error(f"Item with id {item_id} not found")

    return _success(updated_item)


@inventory_bp.route("/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    deleted = store.delete_item(item_id)
    if not deleted:
        return _error(f"Item with id {item_id} not found")

    return _success({"message": f"Item with id {item_id} deleted"})


@inventory_bp.route("/find-by-barcode/<barcode>", methods=["GET"])
def find_by_barcode(barcode):
    product = external_api.fetch_by_barcode(barcode)
    if product is None:
        return _error(f"No product found for barcode {barcode}")
    return _success(product)


@inventory_bp.route("/find-by-name/<name>", methods=["GET"])
def find_by_name(name):
    products = external_api.fetch_by_name(name)
    if not products:
        return _error(f"No product found for name '{name}'")
    return _success(products)
