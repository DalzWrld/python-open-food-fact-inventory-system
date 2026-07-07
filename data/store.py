inventory = []

# Simple counter to hand out unique ids. Starts at 1.
_next_id = 1


def get_all_items():
    return inventory


def get_item_by_id(item_id):
    for item in inventory:
        if item["id"] == item_id:
            return item
    return None


def add_item(data):
    global _next_id

    new_item = {
        "id": _next_id,
        "name": data.get("name", "Unnamed Item"),
        "brand": data.get("brand", ""),
        "barcode": data.get("barcode", ""),
        "price": data.get("price", 0.0),
        "quantity": data.get("quantity", 0),
        "ingredients": data.get("ingredients", ""),
        "source": data.get("source", "manual"),
    }

    inventory.append(new_item)
    _next_id += 1
    return new_item


def update_item(item_id, data):
    item = get_item_by_id(item_id)
    if item is None:
        return None

    for key, value in data.items():
        if key in item and key != "id":
            item[key] = value

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
