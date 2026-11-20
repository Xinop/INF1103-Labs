import csv
from Classes.inventory import Inventory
from Classes.product_factory import ProductFactory
from Classes.supplier import Supplier


def load_products(path: str, inventory: Inventory, supplier: Supplier):
    """Import the lab CSV; report invalid rows and keep valid products."""
    try:
        file = open(path, newline="", encoding="utf-8")
    except FileNotFoundError:
        print(f"Products file not found: {path}")
    else:
        loaded = 0
        with file:
            rows = csv.reader(file)
            next(rows, None)  # Skip the header.
            for row_number, row in enumerate(rows, start=2):
                try:
                    if len(row) != 5:
                        raise ValueError("Expected five columns")
                    product_type, product_id, name, price, stock = row
                    product = ProductFactory.create(
                        product_type, product_id, name, float(price),
                        int(stock), supplier
                    )
                    if not inventory.add_product(product):
                        raise ValueError(f"Product ID already exists: {product_id}")
                except ValueError as error:
                    print(f"Skipping row {row_number}: {error}")
                else:
                    loaded += 1
        print(f"{loaded} products loaded.")
    finally:
        print("Load attempt finished.")


if __name__ == "__main__":
    inventory = Inventory()
    supplier = Supplier("S001", "CSV Supplier", "csv@example.com")
    load_products("products.csv", inventory, supplier)
    inventory.display_all()
