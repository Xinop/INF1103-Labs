from file_handler import FileHandler
from menu import Menu

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
