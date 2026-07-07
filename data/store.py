inventory = []

# Simple counter to hand out unique ids. Starts at 1.
_next_id = 1


def get_all_items():
    """Return every item currently in the inventory."""
    return inventory


def get_item_by_id(item_id):
    """Return a single item matching item_id, or None if not found."""
    for item in inventory:
        if item["id"] == item_id:
            return item
    return None


def add_item(data):
    """
    Add a new item to the inventory.

    'data' should be a dict containing at least 'name'. Missing optional
    fields are filled in with sensible defaults so the shape of every
    item in the array stays consistent.
    """
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
    """
    Update fields on an existing item. Only keys present in 'data'
    are changed; everything else stays the same. Returns the updated
    item, or None if no item with that id exists.
    """
    item = get_item_by_id(item_id)
    if item is None:
        return None

    for key, value in data.items():
        if key in item and key != "id":
            item[key] = value

    return item


def delete_item(item_id):
    """
    Remove an item from the inventory by id.
    Returns True if something was deleted, False if the id wasn't found.
    """
    global inventory

    item = get_item_by_id(item_id)
    if item is None:
        return False

    inventory.remove(item)
    return True


def reset_store():
    """Utility used by the test suite to reset state between tests."""
    global inventory, _next_id
    inventory = []
    _next_id = 1
