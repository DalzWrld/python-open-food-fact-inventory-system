def menu():
    print("""
==========================
Inventory Management
==========================

1. View Inventory
2. View Product
3. Add Product
4. Update Product
5. Delete Product
6. Search Barcode
7. Search Product
8. Exit
""")


def main():
    while True:
        menu()

        choice = input("Choice: ")

        if choice == "8":
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()