import json
from .inventory import Inventory
from .product_types import create_product


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

        except (FileNotFoundError, json.JSONDecodeError):
            inventory_data = []

            with open(self.__file_name, "w") as file:
                json.dump(inventory_data, file, indent=4)

        if not isinstance(inventory_data, list):
            print("Invalid inventory format: expected a list of products.")
            return inventory

        for data in inventory_data:
            try:
                product = create_product(data)
                inventory.add_product(product)

            except (ValueError, KeyError, TypeError) as error:
                print(f"Invalid inventory record skipped: {error}")

        return inventory

    def save_inventory(self, inventory):
        inventory_data = []

        for product in inventory.get_products():
            inventory_data.append(product.to_dictionary())

        with open(self.__file_name, "w") as file:
            json.dump(inventory_data, file, indent=4)

        print(f"Inventory saved successfully to {self.__file_name}.")
