from Classes.file_handler import FileHandler
from Classes.menu import Menu

inventory_file = "inventory.json"


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

file_handler = FileHandler(inventory_file)


# =========================================================
# LOAD INVENTORY
# =========================================================

@load_inventory_decorator
def load_inventory():
    return file_handler.load_inventory()


# =========================================================
# MAIN
# =========================================================

def main():
    inventory = load_inventory.start()
    menu = Menu(inventory, file_handler)
    menu.run()


if __name__ == "__main__":
    main()

# from Classes.product import Product
# from Classes.product_physical import PhysicalProduct
# from Classes.product_digital import DigitalProduct

# physical = PhysicalProduct("P001", "Laptop", 1200.0, 2, 3.0)
# digital = DigitalProduct("D001", "License", 50.0, 10, 850.0)

# print(physical.get_name)
# print(digital)

# print(physical.get_product_id())
# print(isinstance(digital, Product)) 

# physical.display_information()
# digital.display_information()

# print(physical.get_fulfilment_info())
# print(digital.get_fulfilment_info())

# print(physical.calculate_shipping_cost())