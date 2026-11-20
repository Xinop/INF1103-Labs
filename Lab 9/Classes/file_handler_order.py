import json
from pathlib import Path
from .inventory import Inventory
from .order import Order
from .product import Product
from .supplier import Supplier
from product_types import create_product, restore_supplier


class OrderFileHandler:
    """Load and save the orders file."""

    def __init__(self, file_name: str) -> None:
        self.__orders_file: Path = Path(file_name)

    def load_orders(self, inventory: Inventory) -> list[Order]:
        try:
            with self.__orders_file.open("r") as file:
                orders_data = json.load(file)
        except FileNotFoundError:
            return []

        if not isinstance(orders_data, list):
            raise ValueError("Invalid orders format: expected a list of orders.")

        products: dict[str, Product] = {
            product.get_product_id().lower(): product
            for product in inventory.get_products()
        }
        suppliers: dict[str, Supplier] = {
            product.get_supplier().get_supplier_id().lower(): product.get_supplier()
            for product in products.values()
        }
        orders: list[Order] = []
        for data in orders_data:
            order = Order(data["order_id"])
            for line in data["order_lines"]:
                product_data = line["product"]
                product_key = product_data["id"].lower()
                product = products.get(product_key)
                if product is None:
                    # A product can still belong to an order after leaving inventory.
                    supplier = restore_supplier(product_data, suppliers)
                    product = create_product(product_data, supplier)
                    products[product_key] = product

                order.add_order_line(product, line["quantity"])
            orders.append(order)
        return orders

    def save_orders(self, orders: list[Order]) -> None:
        orders_data = [
            {
                "order_id": order.get_order_id(),
                "order_lines": [
                    {
                        "product": line.get_product().to_dictionary(),
                        "quantity": line.get_quantity()
                    }
                    for line in order.get_order_lines()
                ]
            }
            for order in orders
        ]
        with self.__orders_file.open("w") as file:
            json.dump(orders_data, file, indent=4)
        print(f"Orders saved successfully to {self.__orders_file}.")

