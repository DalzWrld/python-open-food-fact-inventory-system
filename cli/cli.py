import argparse
import sys

import requests

BASE_URL = "http://127.0.0.1:5000"
TIMEOUT = 10


def _request(method, path, **kwargs):
    """
    Wrapper around requests that centralizes error handling so every
    command doesn't have to repeat the same try/except block.
    """
    url = f"{BASE_URL}{path}"
    try:
        response = requests.request(method, url, timeout=TIMEOUT, **kwargs)
    except requests.ConnectionError:
        print("Error: could not connect to the API. Is app.py running?")
        sys.exit(1)
    except requests.RequestException as exc:
        print(f"Error: request failed ({exc})")
        sys.exit(1)

    try:
        payload = response.json()
    except ValueError:
        print("Error: API returned a non-JSON response.")
        sys.exit(1)

    return response.status_code, payload


def cmd_list(args):
    status, payload = _request("GET", "/inventory")
    if status != 200:
        print(f"Error: {payload.get('error', 'unknown error')}")
        return

    if not payload:
        print("Inventory is empty.")
        return

    for item in payload:
        print(f"[{item['id']}] {item['name']} - ${item['price']} (qty: {item['quantity']})")


def cmd_view(args):
    status, payload = _request("GET", f"/inventory/{args.item_id}")
    if status != 200:
        print(f"Error: {payload.get('error', 'unknown error')}")
        return

    for key, value in payload.items():
        print(f"{key}: {value}")


def cmd_add(args):
    data = {
        "name": args.name,
        "brand": args.brand,
        "barcode": args.barcode,
        "price": args.price,
        "quantity": args.quantity,
    }
    status, payload = _request("POST", "/inventory", json=data)
    if status != 201:
        print(f"Error: {payload.get('error', 'unknown error')}")
        return

    print(f"Added item [{payload['id']}] {payload['name']}")


def cmd_update(args):
    data = {}
    if args.price is not None:
        data["price"] = args.price
    if args.quantity is not None:
        data["quantity"] = args.quantity
    if args.name is not None:
        data["name"] = args.name

    if not data:
        print("Nothing to update. Provide at least one of --name, --price, --quantity.")
        return

    status, payload = _request("PATCH", f"/inventory/{args.item_id}", json=data)
    if status != 200:
        print(f"Error: {payload.get('error', 'unknown error')}")
        return

    print(f"Updated item [{payload['id']}] {payload['name']}")


def cmd_delete(args):
    status, payload = _request("DELETE", f"/inventory/{args.item_id}")
    if status != 200:
        print(f"Error: {payload.get('error', 'unknown error')}")
        return

    print(payload["message"])


def cmd_find(args):
    if args.barcode:
        status, payload = _request("GET", f"/inventory/lookup/barcode/{args.barcode}")
    elif args.name:
        status, payload = _request("GET", f"/inventory/lookup/name/{args.name}")
    else:
        print("Provide either --barcode or --name to search.")
        return

    if status != 200:
        print(f"Error: {payload.get('error', 'unknown error')}")
        return

    for key, value in payload.items():
        print(f"{key}: {value}")


def cmd_import(args):
    if args.barcode:
        status, payload = _request("POST", f"/inventory/import/barcode/{args.barcode}")
    elif args.name:
        status, payload = _request("POST", f"/inventory/import/name/{args.name}")
    else:
        print("Provide either --barcode or --name to import.")
        return

    if status != 201:
        print(f"Error: {payload.get('error', 'unknown error')}")
        return

    print(f"Imported item [{payload['id']}] {payload['name']} from OpenFoodFacts")


def build_parser():
    parser = argparse.ArgumentParser(
        prog="inventory-cli",
        description="CLI for interacting with the Inventory Management System API",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("list", help="List all inventory items").set_defaults(func=cmd_list)

    view_parser = subparsers.add_parser("view", help="View a single item")
    view_parser.add_argument("item_id", type=int)
    view_parser.set_defaults(func=cmd_view)

    add_parser = subparsers.add_parser("add", help="Add a new inventory item")
    add_parser.add_argument("--name", required=True)
    add_parser.add_argument("--brand", default="")
    add_parser.add_argument("--barcode", default="")
    add_parser.add_argument("--price", type=float, default=0.0)
    add_parser.add_argument("--quantity", type=int, default=0)
    add_parser.set_defaults(func=cmd_add)

    update_parser = subparsers.add_parser("update", help="Update an existing item")
    update_parser.add_argument("item_id", type=int)
    update_parser.add_argument("--name")
    update_parser.add_argument("--price", type=float)
    update_parser.add_argument("--quantity", type=int)
    update_parser.set_defaults(func=cmd_update)

    delete_parser = subparsers.add_parser("delete", help="Delete an item")
    delete_parser.add_argument("item_id", type=int)
    delete_parser.set_defaults(func=cmd_delete)

    find_parser = subparsers.add_parser("find", help="Look up a product on OpenFoodFacts")
    find_parser.add_argument("--barcode")
    find_parser.add_argument("--name")
    find_parser.set_defaults(func=cmd_find)

    import_parser = subparsers.add_parser(
        "import", help="Look up a product on OpenFoodFacts and add it to inventory"
    )
    import_parser.add_argument("--barcode")
    import_parser.add_argument("--name")
    import_parser.set_defaults(func=cmd_import)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
