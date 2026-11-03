import json
from inventory import Inventory
from product import Product


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

