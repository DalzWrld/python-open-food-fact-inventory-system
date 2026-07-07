from flask import Blueprint, request, jsonify

from data import store
from services import external_api

inventory_bp = Blueprint("inventory", __name__, url_prefix="/inventory")

@inventory_bp.route("", methods=["GET"])
def get_all_items():
    return jsonify(store.get_all_items()), 200


@inventory_bp.route("/<int:item_id>", methods=["GET"])
def get_item(item_id):
    item = store.get_item_by_id(item_id)
    if item is None:
        return jsonify({"error": f"Item with id {item_id} not found"}), 404
    return jsonify(item), 200


@inventory_bp.route("", methods=["POST"])
def create_item():
    data = request.get_json(silent=True)
    if not data or "name" not in data:
        return jsonify({"error": "Request body must include at least a 'name' field"}), 400

    new_item = store.add_item(data)
    return jsonify(new_item), 201


@inventory_bp.route("/<int:item_id>", methods=["PATCH"])
def update_item(item_id):
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body must contain JSON fields to update"}), 400

    updated_item = store.update_item(item_id, data)
    if updated_item is None:
        return jsonify({"error": f"Item with id {item_id} not found"}), 404

    return jsonify(updated_item), 200


@inventory_bp.route("/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    deleted = store.delete_item(item_id)
    if not deleted:
        return jsonify({"error": f"Item with id {item_id} not found"}), 404

    return jsonify({"message": f"Item with id {item_id} deleted"}), 200




@inventory_bp.route("/lookup/barcode/<barcode>", methods=["GET"])
def lookup_by_barcode(barcode):
    product = external_api.fetch_by_barcode(barcode)
    if product is None:
        return jsonify({"error": f"No product found for barcode {barcode}"}), 404
    return jsonify(product), 200


@inventory_bp.route("/lookup/name/<name>", methods=["GET"])
def lookup_by_name(name):
    product = external_api.fetch_by_name(name)
    if product is None:
        return jsonify({"error": f"No product found for name '{name}'"}), 404
    return jsonify(product), 200


@inventory_bp.route("/import/barcode/<barcode>", methods=["POST"])
def import_by_barcode(barcode):
    product = external_api.fetch_by_barcode(barcode)
    if product is None:
        return jsonify({"error": f"No product found for barcode {barcode}"}), 404

    new_item = store.add_item(product)
    return jsonify(new_item), 201


@inventory_bp.route("/import/name/<name>", methods=["POST"])
def import_by_name(name):
    product = external_api.fetch_by_name(name)
    if product is None:
        return jsonify({"error": f"No product found for name '{name}'"}), 404

    new_item = store.add_item(product)
    return jsonify(new_item), 201