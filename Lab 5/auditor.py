import json
inventory_file = "inventory.json"

def load_inventory_decorator(func):
    def wrapper():
        inventory = func()
        return inventory

    def start():
        inventory = func()
        print("========================================")
        print("INVENTORY MANAGEMENT SYSTEM")
        print("========================================")
        if len(inventory) == 0:
            print("(No previous inventory found)")
        else:
            print(f"{inventory_file} found.")
            print("Inventory loaded successfully.")
        return inventory

    wrapper.start = start
    return wrapper


@load_inventory_decorator
def load_inventory():
    inventory = []
    try:
        with open(inventory_file, "r") as file:
            inventory = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        inventory = []
        with open(inventory_file, "w") as file:
            json.dump(inventory, file, indent=4)

    return inventory

def save_inventory(inventory):
    with open(inventory_file, "w") as file:
        json.dump(inventory, file, indent=4)

    print("Inventory saved successfully.")


def display_all(inventory):
    print("\n=====Current Inventory=====")

    if len(inventory) == 0:
        print("(No products found)")
        return
    for product in inventory:
        print(
            f"ID: {product['id']} | "
            f"Name: {product['name']} | "
            f"Price: ${product['price']:.2f} | "
            f"Stock: {product['stock']}"
        )
    print("===========================")




def search_product(inventory, product_id):
    for product in inventory:
        if product["id"].lower() == product_id.lower():
            return product
    return None



def add_product(inventory):
    invalid_characters = "[](),"
    print("\n=====Add Product=====")
    while True:
        product_id = input("Product ID: ").strip()
        if not product_id:
            print("Product ID cannot be empty.")
            continue
        if search_product(inventory, product_id):
            print("Product ID already exists.")
            continue
        break

    while True:
        product_name = input("Product Name: ").strip()
        if not product_name:
            print("Product Name cannot be empty.")
            continue
        if any(char in product_name for char in invalid_characters):
            print("Product name contains invalid characters.")
            continue
        break

    while True:
        price_input = input("Price: ").strip()
        if not price_input:
            print("Price cannot be empty.")
            continue
        try:
            price = float(price_input)
            if price < 0:
                print("Price cannot be negative.")
                continue
            break
        except ValueError:
            print("Invalid price.")


    while True:
        stock_input = input("Stock Quantity: ").strip()
        if not stock_input:
            print("Stock cannot be empty.")
            continue
        try:
            stock = int(stock_input)
            if stock < 0:
                print("Stock cannot be negative.")
                continue
            break

        except ValueError:
            print("Invalid stock quantity.")

    product = {
        "id": product_id,
        "name": product_name,
        "price": price,
        "stock": stock,
        "transactions": [stock]
    }

    inventory.append(product)
    print("\nProduct added successfully!")


def update_stock(inventory):
    print("\n=====Update Stock=====")
    product_id = input("Enter Product ID: ").strip()
    product = search_product(inventory, product_id)
    if product is None:
        print("Product not found.")
        return

    print(f"Product Found: {product['name']}")
    print(f"Current Stock: {product['stock']}")

    while True:
        stock_input = input("New Stock Quantity: ").strip()
        if not stock_input:
            print("Stock cannot be empty.")
            continue
        try:
            new_stock = int(stock_input)
            if new_stock < 0:
                print("Stock cannot be negative.")
                continue
            break

        except ValueError:
            print("Invalid stock quantity.")


    old_stock = product["stock"]
    transaction = new_stock - old_stock
    product["stock"] = new_stock
    if "transactions" not in product:
        product["transactions"] = []

    product["transactions"].append(transaction)
    print("Stock updated successfully!")


def search_product_menu(inventory):
    print("\n=====Search Product=====")
    product_id = input("Enter Product ID: ").strip()
    product = search_product(inventory, product_id)
    if product is None:
        print("Product not found.")
        return

    print("\nProduct Found")
    print("========================")
    print(f"ID: {product['id']}")
    print(f"Name: {product['name']}")
    print(f"Price: ${product['price']:.2f}")
    print(f"Stock: {product['stock']}")
    print("========================")

def menu():
    print("\n---------- MENU ----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("--------------------------")


def main():
    inventory = load_inventory.start()
    while True:
        menu()
        option = input("Enter option: ").strip()
        if option == "1":
            display_all(inventory)
            continue
        if option == "2":
            add_product(inventory)
            continue
        if option == "3":
            update_stock(inventory)
            continue
        if option == "4":
            search_product_menu(inventory)
            continue
        if option == "5":
            print("\nSaving inventory...")
            save_inventory(inventory)
            continue
        if option == "6":
            print("\nSaving inventory before exit...")
            save_inventory(inventory)
            print("\nThank you for using Inventory Management System.")
            print("Program terminated.")

            break

        print("Invalid option. Please enter 1 to 6.")


if __name__ == "__main__":
    main()

