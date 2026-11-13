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


def display_orders(orders: list[Order]) -> None:
    if not orders:
        print("\nNo orders found.")
        return
    for order in orders:
        order.display_information()


def find_order(orders: list[Order], order_id: str) -> Order | None:
    for order in orders:
        if order.get_order_id().casefold() == order_id.casefold():
            return order
    return None


def search_order(orders: list[Order]) -> None:
    order_id = input("Enter Order ID: ").strip()
    order = find_order(orders, order_id)
    if order is None:
        print("\nOrder not found.")
        return
    order.display_information()


def update_order(orders: list[Order], inventory: Inventory) -> bool:
    """Return whether an order changed so the menu can save it."""
    order_id = input("Enter Order ID: ").strip()
    order = find_order(orders, order_id)
    if order is None:
        print("\nOrder not found.")
        return False

    changed = False
    while True:
        order.display_information()
        print("Enter a line number to change its quantity or remove it.")
        selection = input("Line number (0 to add a product, blank to finish): ").strip()
        if not selection:
            return changed
        try:
            line_number = int(selection)
        except ValueError:
            print("Please enter a valid line number.")
            continue
        if not 0 <= line_number <= len(order.get_order_lines()):
            print("Order line number not found.")
            continue

        product = None
        if line_number == 0:
            inventory.display_all()
            product_id = input("Product ID (blank to cancel): ").strip()
            if not product_id:
                continue
            product = inventory.find_product(product_id)
            if product is None:
                print("Product not found.")
                continue

        while True:
            prompt = "Quantity: " if line_number == 0 else "New quantity (0 to remove line): "
            try:
                quantity = int(input(prompt).strip())
                if quantity < 0 or (line_number == 0 and quantity == 0):
                    print("Enter a positive quantity." if line_number == 0
                          else "Quantity cannot be negative.")
                    continue
                break
            except ValueError:
                print("Please enter a whole number.")

        if line_number == 0:
            assert product is not None
            order.add_order_line(product, quantity)
        else:
            order.update_order_line(line_number, quantity)
        changed = True
        print("\nOrder updated successfully!")


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
    suppliers_by_id: dict[str, Supplier] = {}
    for product in get_known_products(inventory, orders):
        supplier = product.get_supplier()
        suppliers_by_id[supplier.get_supplier_id().casefold()] = supplier
    suppliers = list(suppliers_by_id.values())

    while True:
        print("\nSupplier")
        print("1. Search by ID")
        print("2. Search by Name")
        print("3. Search by Email")
        print("4. Add New Supplier")
        option = input("Enter option: ").strip()

        if option == "4":
            break
        if option not in ("1", "2", "3"):
            print("Invalid option. Please enter 1 to 4.")
            continue

        label = {"1": "ID", "2": "Name", "3": "Email"}[option]
        query = input(f"Supplier {label}: ").strip().casefold()
        if not query:
            print("Search cannot be empty.")
            continue

        matches: list[Supplier] = []
        for supplier in suppliers:
            if option == "1":
                matched = supplier.get_supplier_id().casefold() == query
            elif option == "2":
                matched = query in supplier.get_name().casefold()
            else:
                matched = query in supplier.get_contact_email().casefold()
            if matched:
                matches.append(supplier)

        if not matches:
            print("Supplier not found. Try another search or add a new supplier.")
            continue

        for number, supplier in enumerate(matches, start=1):
            print(f"{number}. {supplier.get_supplier_id()} | {supplier.get_name()} "
                  f"| {supplier.get_contact_email()}")

        if len(matches) == 1:
            supplier = matches[0]
        else:
            while True:
                selection = input("Select supplier number (blank to search again): ").strip()
                if not selection:
                    break
                try:
                    number = int(selection)
                    if 1 <= number <= len(matches):
                        break
                except ValueError:
                    pass
                print("Please select a listed supplier number.")
            if not selection:
                continue
            supplier = matches[number - 1]

        print(f"Using existing supplier: {supplier.get_name()} ({supplier.get_supplier_id()})")
        return supplier

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


