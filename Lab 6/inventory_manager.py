import json

inventory_file = "inventory.json"


# =========================================================
# PRODUCT CLASS
# =========================================================

class Product:
    def __init__(self, product_id, name, price, stock):
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__stock = stock

    def get_product_id(self):
        return self.__product_id

    def get_name(self):
        return self.__name

    def get_price(self):
        return self.__price

    def get_stock(self):
        return self.__stock

    def update_stock(self, quantity):
        self.__stock = quantity

    def display_information(self):
        print(
            f"ID: {self.__product_id} | "
            f"Name: {self.__name} | "
            f"Price: ${self.__price:.2f} | "
            f"Stock: {self.__stock}"
        )

    def to_dictionary(self):
        return {
            "id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock
        }


# =========================================================
# INVENTORY CLASS
# =========================================================

class Inventory:
    def __init__(self):
        self.__products = []

    def add_product(self, product):
        if self.search_product(product.get_product_id()) is not None:
            return False

        self.__products.append(product)
        return True

    def search_product(self, product_id):
        for product in self.__products:
            if product.get_product_id().lower() == product_id.lower():
                return product

        return None

    def display_all(self):
        print("\nCurrent Inventory")
        print("------------------------------------------")

        if len(self.__products) == 0:
            print("(No products found)")
            print("------------------------------------------")
            return

        for product in self.__products:
            product.display_information()

        print("------------------------------------------")

    def get_products(self):
        return self.__products


# =========================================================
# LOAD INVENTORY DECORATOR
# =========================================================

def load_inventory_decorator(func):
    def wrapper():
        inventory = func()
        return inventory

    def start():
        inventory = func()

        print("========================================")
        print("INVENTORY MANAGEMENT SYSTEM")
        print("========================================")

        if len(inventory.get_products()) == 0:
            print("(No previous inventory found)")
        else:
            print(f"{inventory_file} found.")
            print("Inventory loaded successfully.")

        return inventory

    wrapper.start = start

    return wrapper


# =========================================================
# FILE HANDLING CLASS
# =========================================================

class FileHandler:
    def __init__(self, file_name):
        self.__file_name = file_name

    def load_inventory(self):
        inventory = Inventory()

        try:
            with open(self.__file_name, "r") as file:
                inventory_data = json.load(file)

            for data in inventory_data:
                product = Product(
                    data["id"],
                    data["name"],
                    float(data["price"]),
                    int(data["stock"])
                )

                inventory.add_product(product)

        except (FileNotFoundError, json.JSONDecodeError):
            with open(self.__file_name, "w") as file:
                json.dump([], file, indent=4)

        return inventory

    def save_inventory(self, inventory):
        inventory_data = []

        for product in inventory.get_products():
            inventory_data.append(product.to_dictionary())

        with open(self.__file_name, "w") as file:
            json.dump(inventory_data, file, indent=4)

        print(f"Inventory saved successfully to {self.__file_name}.")


file_handler = FileHandler(inventory_file)


# =========================================================
# LOAD INVENTORY
# =========================================================

@load_inventory_decorator
def load_inventory():
    return file_handler.load_inventory()


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
    print(f"ID: {product.get_product_id()}")
    print(f"Name: {product.get_name()}")
    print(f"Price: ${product.get_price():.2f}")
    print(f"Stock: {product.get_stock()}")
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

    product = Product(product_id, product_name, price, stock)

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


# =========================================================
# MAIN
# =========================================================

def main():
    inventory = load_inventory.start()
    menu = Menu(inventory, file_handler)
    menu.run()


if __name__ == "__main__":
    main()
