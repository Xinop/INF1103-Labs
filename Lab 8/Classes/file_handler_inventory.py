import json
from .inventory import Inventory
from .supplier import Supplier
from product_types import create_product, restore_supplier


class InventoryFileHandler:
    """Load and save the inventory file."""

    def __init__(self, file_name: str) -> None:
        self.__file_name: str = file_name

    def load_inventory(self) -> Inventory:
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

        # Products with the same supplier ID share a Supplier object.
        suppliers: dict[str, Supplier] = {}

        for data in inventory_data:
            try:
                supplier = restore_supplier(data, suppliers)
                product = create_product(data, supplier)
                inventory.add_product(product)

            except (ValueError, KeyError, TypeError, AttributeError) as error:
                print(f"Invalid inventory record skipped: {error}")

        return inventory

    def save_inventory(self, inventory: Inventory) -> None:
        inventory_data: list[dict[str, object]] = []

        for product in inventory.get_products():
            inventory_data.append(product.to_dictionary())

        with open(self.__file_name, "w") as file:
            json.dump(inventory_data, file, indent=4)

        print(f"Inventory saved successfully to {self.__file_name}.")
