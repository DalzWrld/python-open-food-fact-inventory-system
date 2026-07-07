import requests
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

class InventoryCLI:
    def __init__(self, base_url='http://localhost:5000/api'):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json'
        })
    
    def display_menu(self):
        print("\n" + "=" * 50)
        print(" INVENTORY MANAGEMENT SYSTEM - CLI")
        print("="*50)
        print("1. View All Items")
        print("2. View Single Item")
        print("3. Add New Item")
        print("4. Update Item")
        print("5. Delete Item")
        print("6. Search by Barcode (OpenFoodFacts)")
        print("7. Search by Name (OpenFoodFacts)")
        print("8. Fetch Product by Barcode and Add to Inventory")
        print("9. Exit")
        print("=" * 50)
    
    def view_all_items(self):
        try:
            response = self.session.get(f"{self.base_url}/inventory")
            response.raise_for_status()
            data = response.json()
            
            if data['status'] == 'success':
                items = data['data']
                print(f"\n INVENTORY ITEMS ({len(items)})")
                print("-" * 80)
                for item in items:
                    print(f"ID: {item['id']}")
                    print(f"  Name: {item['product_name']}")
                    print(f"  Brand: {item['brands']}")
                    print(f"  Price: ${item['price']:.2f}")
                    print(f"  Quantity: {item['quantity']}")
                    print(f"  Barcode: {item['barcode']}")
                    print("-" * 80)
            else:
                print(f"Error: {data.get('message', 'Unknown error')}")
        except requests.RequestException as e:
            print(f"Error connecting to API: {e}")
    
    def view_single_item(self):
        item_id = input("Enter item ID: ").strip()
        if not item_id:
            print("Item ID cannot be empty")
            return
        
        try:
            response = self.session.get(f"{self.base_url}/inventory/{item_id}")
            response.raise_for_status()
            data = response.json()
            
            if data['status'] == 'success':
                item = data['data']
                print("\n ITEM DETAILS")
                print("-" * 80)
                print(f"ID: {item['id']}")
                print(f"Name: {item['product_name']}")
                print(f"Brand: {item['brands']}")
                print(f"Price: ${item['price']:.2f}")
                print(f"Quantity: {item['quantity']}")
                print(f"Barcode: {item['barcode']}")
                print(f"Ingredients: {item['ingredients_text'][:100]}...")
                print(f"Created: {item['created_at']}")
                print(f"Updated: {item['updated_at']}")
                print("-" * 80)
            else:
                print(f"Error: {data.get('message', 'Unknown error')}")
        except requests.RequestException as e:
            print(f"Error connecting to API: {e}")
    
    def add_new_item(self):
        print("\n ADD NEW ITEM")
        print("-" * 50)
        
        product_name = input("Product Name: ").strip()
        if not product_name:
            print("Product name cannot be empty")
            return
        
        brands = input("Brand: ").strip() or "Unknown"
        price = input("Price: ").strip()
        try:
            price = float(price)
        except ValueError:
            print("Invalid price format. Please use a number.")
            return
        
        quantity = input("Quantity: ").strip()
        try:
            quantity = int(quantity)
        except ValueError:
            print("Invalid quantity format. Please use a whole number.")
            return
        
        barcode = input("Barcode (optional): ").strip()
        ingredients = input("Ingredients (optional): ").strip()
        
        item_data = {
            'product_name': product_name,
            'brands': brands,
            'price': price,
            'quantity': quantity,
            'barcode': barcode,
            'ingredients_text': ingredients
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/inventory",
                json=item_data
            )
            response.raise_for_status()
            data = response.json()
            
            if data['status'] == 'success':
                print("Item added successfully!")
                print(f"ID: {data['data']['id']}")
            else:
                print(f"Error: {data.get('message', 'Unknown error')}")
        except requests.RequestException as e:
            print(f"Error connecting to API: {e}")
    
    def update_item(self):
        item_id = input("Enter item ID to update: ").strip()
        if not item_id:
            print("Item ID cannot be empty")
            return
        
        print("\n UPDATE ITEM (leave blank to keep current value)")
        print("-" * 50)
        
        
        try:
            response = self.session.get(f"{self.base_url}/inventory/{item_id}")
            response.raise_for_status()
            data = response.json()
            if data['status'] == 'success':
                current_item = data['data']
                print(f"Current Name: {current_item['product_name']}")
                print(f"Current Brand: {current_item['brands']}")
                print(f"Current Price: ${current_item['price']:.2f}")
                print(f"Current Quantity: {current_item['quantity']}")
                print(f"Current Barcode: {current_item['barcode']}")
                print("-" * 50)
                
                updates = {}
                
                product_name = input("New Product Name: ").strip()
                if product_name:
                    updates['product_name'] = product_name
                
                brands = input("New Brand: ").strip()
                if brands:
                    updates['brands'] = brands
                
                price = input("New Price: ").strip()
                if price:
                    try:
                        updates['price'] = float(price)
                    except ValueError:
                        print("Invalid price format. Skipping price update.")
                
                quantity = input("New Quantity: ").strip()
                if quantity:
                    try:
                        updates['quantity'] = int(quantity)
                    except ValueError:
                        print("Invalid quantity format. Skipping quantity update.")
                
                barcode = input("New Barcode: ").strip()
                if barcode:
                    updates['barcode'] = barcode
                
                if not updates:
                    print("No updates provided.")
                    return
                
                response = self.session.patch(
                    f"{self.base_url}/inventory/{item_id}",
                    json=updates
                )
                response.raise_for_status()
                data = response.json()
                
                if data['status'] == 'success':
                    print("Item updated successfully!")
                else:
                    print(f"Error: {data.get('message', 'Unknown error')}")
            else:
                print(f"Error: {data.get('message', 'Unknown error')}")
        except requests.RequestException as e:
            print(f"Error connecting to API: {e}")
    
    def delete_item(self):
        item_id = input("Enter item ID to delete: ").strip()
        if not item_id:
            print("Item ID cannot be empty")
            return
        
        confirm = input(f"Are you sure you want to delete item {item_id}? (y/n): ").strip().lower()
        if confirm != 'y':
            print("Deletion cancelled")
            return
        
        try:
            response = self.session.delete(f"{self.base_url}/inventory/{item_id}")
            response.raise_for_status()
            data = response.json()
            
            if data['status'] == 'success':
                print("Item deleted successfully!")
            else:
                print(f"Error: {data.get('message', 'Unknown error')}")
        except requests.RequestException as e:
            print(f"Error connecting to API: {e}")
    
    def search_by_barcode(self):
        barcode = input("Enter barcode: ").strip()
        if not barcode:
            print("Barcode cannot be empty")
            return
        
        try:
            response = self.session.get(f"{self.base_url}/inventory/find-by-barcode/{barcode}")
            response.raise_for_status()
            data = response.json()
            
            if data['status'] == 'success':
                product = data['data']
                print("\n PRODUCT FOUND")
                print("-" * 80)
                print(f"Name: {product['product_name']}")
                print(f"Brand: {product['brands']}")
                print(f"Barcode: {product['barcode']}")
                print(f"Ingredients: {product['ingredients_text'][:200]}...")
                print("-" * 80)
            else:
                print(f"Error: {data.get('message', 'Unknown error')}")
        except requests.RequestException as e:
            print(f"Error connecting to API: {e}")
    
    def search_by_name(self):
        product_name = input("Enter product name to search: ").strip()
        if not product_name:
            print("Product name cannot be empty")
            return
        
        try:
            response = self.session.get(
                f"{self.base_url}/inventory/find-by-name/{product_name}"
            )
            response.raise_for_status()
            data = response.json()
            
            if data['status'] == 'success':
                products = data['data']
                print(f"\n SEARCH RESULTS ({len(products)})")
                print("-" * 80)
                for i, product in enumerate(products, 1):
                    print(f"{i}. Name: {product['product_name']}")
                    print(f"   Brand: {product['brands']}")
                    print(f"   Barcode: {product['barcode']}")
                    print("-" * 40)
            else:
                print(f"Error: {data.get('message', 'Unknown error')}")
        except requests.RequestException as e:
            print(f"Error connecting to API: {e}")
    
    def fetch_and_add_product(self):
        barcode = input("Enter barcode: ").strip()
        if not barcode:
            print("Barcode cannot be empty")
            return
        
        price = input("Enter price (optional, press Enter to set to 0): ").strip()
        price = float(price) if price else 0.0
        
        quantity = input("Enter quantity (optional, press Enter to set to 0): ").strip()
        quantity = int(quantity) if quantity else 0
        
        try:
            response = self.session.get(f"{self.base_url}/inventory/find-by-barcode/{barcode}")
            response.raise_for_status()
            data = response.json()
            
            if data['status'] == 'success':
                product = data['data']
                
                item_data = {
                    'product_name': product['product_name'],
                    'brands': product['brands'],
                    'price': price,
                    'quantity': quantity,
                    'barcode': product['barcode'],
                    'ingredients_text': product['ingredients_text']
                }
                
                response = self.session.post(
                    f"{self.base_url}/inventory",
                    json=item_data
                )
                response.raise_for_status()
                data = response.json()
                
                if data['status'] == 'success':
                    print("Product fetched and added to inventory!")
                    print(f"ID: {data['data']['id']}")
                else:
                    print(f"Error adding to inventory: {data.get('message', 'Unknown error')}")
            else:
                print(f"Error: {data.get('message', 'Product not found')}")
        except requests.RequestException as e:
            print(f"Error connecting to API: {e}")
    
    def run(self):
        print("\n Starting Inventory Management System CLI")
        print("Ensure the Flask server is running on http://localhost:5000")
        
        while True:
            self.display_menu()
            choice = input("\n Select an option (1-9): ").strip()
            
            if choice == '1':
                self.view_all_items()
            elif choice == '2':
                self.view_single_item()
            elif choice == '3':
                self.add_new_item()
            elif choice == '4':
                self.update_item()
            elif choice == '5':
                self.delete_item()
            elif choice == '6':
                self.search_by_barcode()
            elif choice == '7':
                self.search_by_name()
            elif choice == '8':
                self.fetch_and_add_product()
            elif choice == '9':
                print("\n Goodbye!")
                break
            else:
                print("Invalid option. Please choose 1-9.")
            
            input("\n Press Enter to continue...")

def main():
    cli = InventoryCLI()
    cli.run()

if __name__ == "__main__":
    main()