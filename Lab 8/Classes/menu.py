from .inventory import Inventory
from .file_handler_inventory import InventoryFileHandler
from .file_handler_order import OrderFileHandler
from .order import Order
from menu_functions import add_product, display_all, next_id, search_product, update_stock


# =========================================================
# MENU CLASS
# =========================================================

class Menu:
    def __init__(self, inventory: Inventory,
                 inventory_file_handler: InventoryFileHandler,
                 order_file_handler: OrderFileHandler) -> None:
        self.inventory: Inventory = inventory
        self.inventory_file_handler: InventoryFileHandler = inventory_file_handler
        self.order_file_handler: OrderFileHandler = order_file_handler
        self.orders: list[Order] = self.order_file_handler.load_orders(inventory)

    def create_order(self) -> None:
        if not self.inventory.get_products():
            print("\nAdd products to the inventory before creating an order.")
            return

        print("\nCreate Order")

        order_id = next_id("O", [order.get_order_id() for order in self.orders])
        print(f"Assigned Order ID: {order_id}")

        order = Order(order_id)
        self.inventory.display_all()

        while True:
            product_id = input("Product ID (blank to finish): ").strip()
            if not product_id:
                break

            product = self.inventory.find_product(product_id)
            if product is None:
                print("Product not found.")
                continue

            while True:
                try:
                    quantity = int(input("Quantity: ").strip())
                    if quantity <= 0:
                        print("Quantity must be a positive integer.")
                        continue
                    break
                except ValueError:
                    print("Quantity must be a positive integer.")

            # The Order creates and owns its OrderLine objects.
            order.add_order_line(product, quantity)
            print(f"Added {quantity} x {product.get_name()}.")

        if not order.get_order_lines():
            print("Order cancelled: no products were added.")
            return

        self.orders.append(order)
        self.order_file_handler.save_orders(self.orders)
        print("\nOrder created successfully!")
        order.display_information()

    def menu(self) -> None:
        print("\n---------- MENU ----------")
        print("1. Display All Products")
        print("2. Add Product")
        print("3. Update Stock")
        print("4. Search Product")
        print("5. Save Inventory")
        print("6. Create Order")
        print("7. Exit")
        print("--------------------------")

    def run(self) -> None:
        while True:
            self.menu()

            option = input("\nEnter option: ").strip()

            if option == "1":
                display_all(self.inventory)
                continue

            if option == "2":
                add_product(self.inventory, self.orders)
                continue

            if option == "3":
                update_stock(self.inventory)
                continue

            if option == "4":
                search_product(self.inventory)
                continue

            if option == "5":
                print("\nSaving inventory...")
                self.inventory_file_handler.save_inventory(self.inventory)
                self.order_file_handler.save_orders(self.orders)
                continue

            if option == "6":
                self.create_order()
                continue

            if option == "7":
                print("\nSaving inventory before exit...")
                self.inventory_file_handler.save_inventory(self.inventory)
                self.order_file_handler.save_orders(self.orders)

                print("\nThank you for using Inventory Management System.")
                print("Program terminated.")
                break

            print("Invalid option. Please enter 1 to 7.")
