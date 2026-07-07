from flask import Blueprint, request, jsonify
import uuid
from datetime import datetime
from app.services.openfoodfacts import OpenFoodFactsService

inventory_bp = Blueprint('inventory', __name__)

inventory_db = [
    {
        'id': '1',
        'product_name': 'Organic Almond Milk',
        'brands': 'Silk',
        'ingredients_text': 'Filtered water, almonds, cane sugar, sea salt, natural flavors, carrageenan, sunflower lecithin, vitamin E, vitamin D2',
        'barcode': '1234567890123',
        'price': 4.99,
        'quantity': 50,
        'created_at': '2026-01-15T10:30:00',
        'updated_at': '2026-01-15T10:30:00'
    },
    {
        'id': '2',
        'product_name': 'Classic Oatmeal',
        'brands': 'Quaker',
        'ingredients_text': 'Whole grain rolled oats, salt, calcium carbonate, iron, vitamin A, vitamin C',
        'barcode': '9876543210987',
        'price': 3.49,
        'quantity': 100,
        'created_at': '2026-01-15T11:00:00',
        'updated_at': '2026-01-15T11:00:00'
    }
]

openfoodfacts_service = OpenFoodFactsService()


@inventory_bp.route('/inventory', methods=['GET'])
def get_all_items():
    try:
        return jsonify({
            'status': 'success',
            'data': inventory_db,
            'count': len(inventory_db)
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@inventory_bp.route('/inventory/<item_id>', methods=['GET'])
def get_single_item(item_id):
    try:
        item = next((item for item in inventory_db if item['id'] == item_id), None)
        if not item:
            return jsonify({
                'status': 'error',
                'message': f'Item with ID {item_id} not found'
            }), 404
        
        return jsonify({
            'status': 'success',
            'data': item
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@inventory_bp.route('/inventory', methods=['POST'])
def add_item():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['product_name', 'price', 'quantity']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'status': 'error',
                    'message': f'Missing required field: {field}'
                }), 400
        
        # Create new item
        new_item = {
            'id': str(uuid.uuid4()),
            'product_name': data['product_name'],
            'brands': data.get('brands', ''),
            'ingredients_text': data.get('ingredients_text', ''),
            'barcode': data.get('barcode', ''),
            'price': float(data['price']),
            'quantity': int(data['quantity']),
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        
        # If barcode provided, try to fetch additional data from OpenFoodFacts
        if data.get('barcode'):
            product_data = openfoodfacts_service.get_product_by_barcode(data['barcode'])
            if product_data:
                # Enhance with API data if available
                new_item['product_name'] = product_data.get('product_name', new_item['product_name'])
                new_item['brands'] = product_data.get('brands', new_item['brands'])
                new_item['ingredients_text'] = product_data.get('ingredients_text', new_item['ingredients_text'])
        
        inventory_db.append(new_item)
        
        return jsonify({
            'status': 'success',
            'message': 'Item added successfully',
            'data': new_item
        }), 201
        
    except ValueError as e:
        return jsonify({
            'status': 'error',
            'message': f'Invalid data type: {str(e)}'
        }), 400
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@inventory_bp.route('/inventory/<item_id>', methods=['PATCH'])
def update_item(item_id):
    """Update an existing inventory item"""
    try:
        data = request.get_json()
        
        # Find the item
        item = next((item for item in inventory_db if item['id'] == item_id), None)
        if not item:
            return jsonify({
                'status': 'error',
                'message': f'Item with ID {item_id} not found'
            }), 404
        
        # Update allowed fields
        allowed_fields = ['product_name', 'brands', 'ingredients_text', 'price', 'quantity', 'barcode']
        
        for field in allowed_fields:
            if field in data:
                if field in ['price', 'quantity']:
                    # Convert to appropriate type
                    item[field] = float(data[field]) if field == 'price' else int(data[field])
                else:
                    item[field] = data[field]
        
        # Update timestamp
        item['updated_at'] = datetime.now().isoformat()
        
        # If barcode updated, try to fetch additional data from OpenFoodFacts
        if 'barcode' in data and data['barcode']:
            product_data = openfoodfacts_service.get_product_by_barcode(data['barcode'])
            if product_data:
                item['product_name'] = product_data.get('product_name', item['product_name'])
                item['brands'] = product_data.get('brands', item['brands'])
                item['ingredients_text'] = product_data.get('ingredients_text', item['ingredients_text'])
        
        return jsonify({
            'status': 'success',
            'message': 'Item updated successfully',
            'data': item
        }), 200
        
    except ValueError as e:
        return jsonify({
            'status': 'error',
            'message': f'Invalid data type: {str(e)}'
        }), 400
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@inventory_bp.route('/inventory/<item_id>', methods=['DELETE'])
def delete_item(item_id):
    """Delete an inventory item"""
    try:
        # Find the item
        item = next((item for item in inventory_db if item['id'] == item_id), None)
        if not item:
            return jsonify({
                'status': 'error',
                'message': f'Item with ID {item_id} not found'
            }), 404
        
        # Remove item
        inventory_db.remove(item)
        
        return jsonify({
            'status': 'success',
            'message': f'Item with ID {item_id} deleted successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@inventory_bp.route('/inventory/find-by-barcode/<barcode>', methods=['GET'])
def find_by_barcode(barcode):
    """Search for product by barcode from OpenFoodFacts API"""
    try:
        product_data = openfoodfacts_service.get_product_by_barcode(barcode)
        
        if not product_data:
            return jsonify({
                'status': 'error',
                'message': f'Product with barcode {barcode} not found in OpenFoodFacts'
            }), 404
        
        # Create a formatted product response
        formatted_product = {
            'product_name': product_data.get('product_name', 'Unknown'),
            'brands': product_data.get('brands', 'Unknown'),
            'ingredients_text': product_data.get('ingredients_text', ''),
            'barcode': barcode
        }
        
        return jsonify({
            'status': 'success',
            'data': formatted_product
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Failed to fetch product: {str(e)}'
        }), 500


@inventory_bp.route('/inventory/find-by-name/<product_name>', methods=['GET'])
def find_by_name(product_name):
    """Search for product by name from OpenFoodFacts API"""
    try:
        products = openfoodfacts_service.get_product_by_name(product_name)
        
        if not products:
            return jsonify({
                'status': 'error',
                'message': f'No products found with name containing "{product_name}"'
            }), 404
        
        # Format products for response
        formatted_products = []
        for product in products[:5]:  # Limit to 5 results
            formatted_products.append({
                'product_name': product.get('product_name', 'Unknown'),
                'brands': product.get('brands', 'Unknown'),
                'ingredients_text': product.get('ingredients_text', ''),
                'barcode': product.get('_id', '')
            })
        
        return jsonify({
            'status': 'success',
            'data': formatted_products,
            'count': len(formatted_products)
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Failed to fetch products: {str(e)}'
        }), 500