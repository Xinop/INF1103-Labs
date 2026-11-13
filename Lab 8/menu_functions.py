from Classes.can_be_shipped import CanBeShipped
from Classes.supplier import Supplier
from Classes.inventory import Inventory
from Classes.order import Order
from Classes.product import Product
from product_types import PRODUCT_TYPES


# =========================================================
# DISPLAY ALL PRODUCTS
# =========================================================

def display_all(inventory: Inventory) -> None:
    inventory.display_all()


# =========================================================
# SEARCH PRODUCT
# =========================================================

def search_product(inventory: Inventory) -> None:
    print("\nSearch Product")

    product_id = input("Enter Product ID: ").strip()

    product = inventory.search_product(product_id)

    if product is None:
        print("\nProduct not found.")
        return

    print("\nProduct Found")
    print("------------------------------------------")
    product.display_information()
    product.display_supplier_information()
    print(f"Fulfilment: {product.get_fulfilment_info()}")

    if isinstance(product, CanBeShipped):
        print(f"Shipping Cost: ${product.calculate_shipping_cost():.2f}")

    print("------------------------------------------")


# =========================================================
# GET SUPPLIER (ASSOCIATION)
# =========================================================

def get_known_products(inventory: Inventory, orders: list[Order] | None = None) -> list[Product]:
    products = list(inventory.get_products())
    for order in orders or []:
        products.extend(line.get_product() for line in order.get_order_lines())
    return products


def next_id(prefix: str, existing_ids: list[str]) -> str:
    numbers = [
        int(identifier[len(prefix):])
        for identifier in existing_ids
        if identifier.upper().startswith(prefix)
        and identifier[len(prefix):].isascii()
        and identifier[len(prefix):].isdigit()
    ]
    return f"{prefix}{max(numbers, default=0) + 1:03d}"


def get_supplier_input(inventory: Inventory, orders: list[Order] | None = None) -> Supplier:

    while True:
        supplier_name = input("Supplier Name: ").strip()

        if supplier_name:
            break

        print("Supplier Name cannot be empty.")

    while True:
        contact_email = input("Supplier Contact Email: ").strip()

        if contact_email and "@" in contact_email:
            break

        print("Please enter a valid supplier contact email.")

    suppliers = [product.get_supplier() for product in get_known_products(inventory, orders)]
    for supplier in suppliers:
        if (supplier.get_name().casefold() == supplier_name.casefold()
                and supplier.get_contact_email().casefold() == contact_email.casefold()):
            print(f"Using existing supplier: {supplier.get_name()} ({supplier.get_supplier_id()})")
            return supplier

    supplier_id = next_id("S", [supplier.get_supplier_id() for supplier in suppliers])
    print(f"Assigned Supplier ID: {supplier_id}")
    return Supplier(supplier_id, supplier_name, contact_email)


# =========================================================
# ADD PRODUCT
# =========================================================

def add_product(inventory: Inventory, orders: list[Order] | None = None) -> None:
    invalid_characters = "[](),"

    print("\nAdd New Product")

    product_id = next_id("P", [
        product.get_product_id() for product in get_known_products(inventory, orders)
    ])
    print(f"Assigned Product ID: {product_id}")

    while True:
        product_name = input("Product Name: ").strip()

        if not product_name:
            print("Product Name cannot be empty.")
            continue

        if any(char in product_name for char in invalid_characters):
            print("Product name contains invalid characters.")
            continue

        break

    while True:
        price_input = input("Price: ").strip()

        if not price_input:
            print("Price cannot be empty.")
            continue

        try:
            price = float(price_input)

            if price < 0:
                print("Price cannot be negative.")
                continue

            break

        except ValueError:
            print("Invalid price. Please enter a number.")
            continue

    while True:
        stock_input = input("Stock Quantity: ").strip()

        if not stock_input:
            print("Stock cannot be empty.")
            continue

        try:
            stock = int(stock_input)

            if stock < 0:
                print("Stock cannot be negative.")
                continue

            break

        except ValueError:
            print("Invalid stock quantity. Please enter an integer.")
            continue

    # -------------------------
    # Choose product type
    # -------------------------

    while True:
        print()
        for product_info in PRODUCT_TYPES.values():
            print(f"{product_info['option']}. {product_info['label']}")

        product_type = input("Enter Product Type: ").strip()
        selected_type = next(
            (info for info in PRODUCT_TYPES.values() if info["option"] == product_type),
            None
        )

        if selected_type is not None:
            break

        print("Invalid product type. Please select a listed option.")

    while True:
        extra_input = input(selected_type["prompt"]).strip()

        if not extra_input:
            print("This field cannot be empty.")
            continue

        try:
            extra_value = selected_type["convert"](extra_input)

            if extra_value < selected_type["minimum"]:
                print("Value must be at least " + str(selected_type["minimum"]) + ".")
                continue

            break

        except ValueError:
            print("Invalid input. Please enter a valid number.")
            continue

    supplier = get_supplier_input(inventory, orders)

    product = selected_type["class"](
        product_id, product_name, price, stock, extra_value, supplier
    )

    if inventory.add_product(product):
        print("\nProduct added successfully!")


# =========================================================
# UPDATE STOCK
# =========================================================

def update_stock(inventory: Inventory) -> None:
    print("\nUpdate Stock")

    product_id = input("Enter Product ID: ").strip()

    product = inventory.search_product(product_id)

    if product is None:
        print("\nProduct not found.")
        return

    print("\nProduct Found:")
    print(f"Name: {product.get_name()}")
    print(f"Current Stock: {product.get_stock()}")

    while True:
        stock_input = input("\nNew Stock Quantity: ").strip()

        if not stock_input:
            print("Stock cannot be empty.")
            continue

        try:
            quantity = int(stock_input)

            if quantity < 0:
                print("Stock cannot be negative.")
                continue

            break

        except ValueError:
            print("Invalid stock quantity. Please enter an integer.")
            continue

    product.update_stock(quantity)

    print("\nStock updated successfully!")


