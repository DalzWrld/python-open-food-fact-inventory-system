from datetime import datetime, timezone

inventory = []
_next_id = 1


def _timestamp():
    return datetime.now(timezone.utc).isoformat()


def get_all_items():
    return inventory


def get_item_by_id(item_id):
    for item in inventory:
        if item["id"] == item_id:
            return item
    return None


def add_item(data):
    global _next_id

    now = _timestamp()
    new_item = {
        "id": _next_id,
        "product_name": data.get("product_name", "Unnamed Item"),
        "brands": data.get("brands", ""),
        "barcode": data.get("barcode", ""),
        "price": data.get("price", 0.0),
        "quantity": data.get("quantity", 0),
        "ingredients_text": data.get("ingredients_text", ""),
        "source": data.get("source", "manual"),
        "created_at": now,
        "updated_at": now,
    }

    inventory.append(new_item)
    _next_id += 1
    return new_item


def update_item(item_id, data):
    item = get_item_by_id(item_id)
    if item is None:
        return None

    for key, value in data.items():
        if key in item and key not in ("id", "created_at"):
            item[key] = value

    item["updated_at"] = _timestamp()
    return item


def delete_item(item_id):
    global inventory

    item = get_item_by_id(item_id)
    if item is None:
        return False

    inventory.remove(item)
    return True


def reset_store():
    global inventory, _next_id
    inventory = []
    _next_id = 1
