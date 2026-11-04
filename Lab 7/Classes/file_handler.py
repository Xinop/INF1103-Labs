import json
from .inventory import Inventory
from .product_digital import DigitalProduct
from .product_physical import PhysicalProduct


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

        for data in inventory_data:
            product_type = data.get("type", "physical")

            if product_type == "physical":
                product = PhysicalProduct(
                    data["id"],
                    data["name"],
                    float(data["price"]),
                    int(data["stock"]),
                    float(data.get("weight", 0))
                )
                inventory.add_product(product)
                continue

            if product_type == "digital":
                product = DigitalProduct(
                    data["id"],
                    data["name"],
                    float(data["price"]),
                    int(data["stock"]),
                    float(data["download_size"])
                )
                inventory.add_product(product)
                continue

            print(f"Unknown product type: {product_type}")

        return inventory

    def save_inventory(self, inventory):
        inventory_data = []

        for product in inventory.get_products():
            inventory_data.append(product.to_dictionary())

        with open(self.__file_name, "w") as file:
            json.dump(inventory_data, file, indent=4)

        print(f"Inventory saved successfully to {self.__file_name}.")