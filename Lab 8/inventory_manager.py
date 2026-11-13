from collections.abc import Callable
from typing import Protocol, cast

from Classes.file_handler_inventory import InventoryFileHandler
from Classes.file_handler_order import OrderFileHandler
from Classes.inventory import Inventory
from Classes.menu import Menu

inventory_file: str = "inventory.json"


class InventoryLoader(Protocol):
    """A callable inventory loader with a startup display operation."""

    start: Callable[[], Inventory]

    def __call__(self) -> Inventory: ...


# =========================================================
# LOAD INVENTORY DECORATOR
# =========================================================

def load_inventory_decorator(func: Callable[[], Inventory]) -> InventoryLoader:
    def wrapper() -> Inventory:
        inventory = func()
        return inventory

    def start() -> Inventory:
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

    loader = cast(InventoryLoader, wrapper)
    loader.start = start

    return loader

inventory_file_handler = InventoryFileHandler(inventory_file)
order_file_handler = OrderFileHandler("orders.json")


# =========================================================
# LOAD INVENTORY
# =========================================================

@load_inventory_decorator
def load_inventory() -> Inventory:
    return inventory_file_handler.load_inventory()


# =========================================================
# MAIN
# =========================================================

def main() -> None:
    inventory = load_inventory.start()
    menu = Menu(inventory, inventory_file_handler, order_file_handler)
    menu.run()


if __name__ == "__main__":
    main()

# from Classes.product import Product
# from Classes.product_physical import PhysicalProduct
# from Classes.product_digital import DigitalProduct

# physical = PhysicalProduct("P001", "Laptop", 1200.0, 2, 3.0)
# digital = DigitalProduct("P002", "License", 50.0, 10, 850.0)

# print(physical.get_name)
# print(digital)

# print(physical.get_product_id())
# print(isinstance(digital, Product)) 

# physical.display_information()
# digital.display_information()

# print(physical.get_fulfilment_info())
# print(digital.get_fulfilment_info())

# print(physical.calculate_shipping_cost())
