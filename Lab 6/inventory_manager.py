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


