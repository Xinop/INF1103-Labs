from .can_be_shipped import CanBeShipped
from .product_types import PRODUCT_TYPES


# =========================================================
# DISPLAY ALL PRODUCTS
# =========================================================

def display_all(inventory):
    inventory.display_all()


# =========================================================
# SEARCH PRODUCT
# =========================================================

def search_product(inventory):
    print("\nSearch Product")

    product_id = input("Enter Product ID: ").strip()

    product = inventory.search_product(product_id)

    if product is None:
        print("\nProduct not found.")
        return

    print("\nProduct Found")
    print("------------------------------------------")
    product.display_information()
    print(f"Fulfilment: {product.get_fulfilment_info()}")

    if isinstance(product, CanBeShipped):
        print(f"Shipping Cost: ${product.calculate_shipping_cost():.2f}")

    print("------------------------------------------")


# =========================================================
# ADD PRODUCT
# =========================================================

def add_product(inventory):
    invalid_characters = "[](),"

    print("\nAdd New Product")

    while True:
        product_id = input("Product ID: ").strip()

        if not product_id:
            print("Product ID cannot be empty.")
            continue

        if inventory.search_product(product_id) is not None:
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
            print("Invalid price. Please enter a number.")
            continue

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
            print("Invalid stock quantity. Please enter an integer.")
            continue

    # -------------------------
    # Choose product type
    # -------------------------

    while True:
        print()
        for product_info in PRODUCT_TYPES.values():
            print(f"{product_info['option']}. {product_info['label']}")

        product_type = input("Enter Product Type: ").strip()
        selected_type = next(
            (info for info in PRODUCT_TYPES.values() if info["option"] == product_type),
            None
        )

        if selected_type is not None:
            break

        print("Invalid product type. Please select a listed option.")

    while True:
        extra_input = input(selected_type["prompt"]).strip()

        if not extra_input:
            print("This field cannot be empty.")
            continue

        try:
            extra_value = selected_type["convert"](extra_input)

            if extra_value < selected_type["minimum"]:
                print("Value must be at least " + str(selected_type["minimum"]) + ".")
                continue

            break

        except ValueError:
            print("Invalid input. Please enter a valid number.")
            continue

    product = selected_type["class"](
        product_id, product_name, price, stock, extra_value
    )

    if inventory.add_product(product):
        print("\nProduct added successfully!")


# =========================================================
# UPDATE STOCK
# =========================================================

def update_stock(inventory):
    print("\nUpdate Stock")

    product_id = input("Enter Product ID: ").strip()

    product = inventory.search_product(product_id)

    if product is None:
        print("\nProduct not found.")
        return

    print("\nProduct Found:")
    print(f"Name: {product.get_name()}")
    print(f"Current Stock: {product.get_stock()}")

    while True:
        stock_input = input("\nNew Stock Quantity: ").strip()

        if not stock_input:
            print("Stock cannot be empty.")
            continue

        try:
            quantity = int(stock_input)

            if quantity < 0:
                print("Stock cannot be negative.")
                continue

            break

        except ValueError:
            print("Invalid stock quantity. Please enter an integer.")
            continue

    product.update_stock(quantity)

    print("\nStock updated successfully!")


# =========================================================
# MENU CLASS
# =========================================================

class Menu:
    def __init__(self, inventory, file_handler):
        self.inventory = inventory
        self.file_handler = file_handler

    def menu(self):
        print("\n---------- MENU ----------")
        print("1. Display All Products")
        print("2. Add Product")
        print("3. Update Stock")
        print("4. Search Product")
        print("5. Save Inventory")
        print("6. Exit")
        print("--------------------------")

    def run(self):
        while True:
            self.menu()

            option = input("\nEnter option: ").strip()

            if option == "1":
                display_all(self.inventory)
                continue

            if option == "2":
                add_product(self.inventory)
                continue

            if option == "3":
                update_stock(self.inventory)
                continue

            if option == "4":
                search_product(self.inventory)
                continue

            if option == "5":
                print("\nSaving inventory...")
                self.file_handler.save_inventory(self.inventory)
                continue

            if option == "6":
                print("\nSaving inventory before exit...")
                self.file_handler.save_inventory(self.inventory)

                print("\nThank you for using Inventory Management System.")
                print("Program terminated.")
                break

            print("Invalid option. Please enter 1 to 6.")
