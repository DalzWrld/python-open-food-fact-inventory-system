from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/inventory/data", methods=["GET"])
def get_inventory():
    pass