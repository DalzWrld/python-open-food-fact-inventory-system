from flask import Flask, jsonify
from routes.inventory import inventory_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(inventory_bp)

    @app.route("/")
    def index():
        return jsonify({
            "message": "Inventory Management System API",
            "endpoints": {
                "GET /inventory": "list all items",
                "GET /inventory/<id>": "get a single item",
                "POST /inventory": "create an item",
                "PATCH /inventory/<id>": "update an item",
                "DELETE /inventory/<id>": "delete an item",
                "GET /inventory/lookup/barcode/<barcode>": "preview OpenFoodFacts data",
                "GET /inventory/lookup/name/<name>": "preview OpenFoodFacts data",
                "POST /inventory/import/barcode/<barcode>": "fetch + add to inventory",
                "POST /inventory/import/name/<name>": "fetch + add to inventory",
            },
        })

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)