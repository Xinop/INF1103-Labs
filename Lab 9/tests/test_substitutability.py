"""Report polymorphism and normal inventory operations for both subclasses."""

import io
import unittest
from contextlib import redirect_stdout

from Classes.inventory import Inventory
from Classes.product import Product
from Classes.product_factory import ProductFactory
from Classes.supplier import Supplier
from tests.reporting import show_case


def show_product_details(product: Product):
    product.display_information()
    print(product.get_fulfilment_info())


def test_substitutability():
    supplier = Supplier("S001", "Tech Supplier", "sales@example.com")
    physical = ProductFactory.create(
        "physical", "P001", "Laptop", 1200.0, 5, supplier, weight=2.5
    )
    digital = ProductFactory.create(
        "digital", "D001", "Software Licence", 50.0, 10, supplier,
        download_size=850.0,
    )

    details_output = io.StringIO()
    with redirect_stdout(details_output):
        show_product_details(physical)
        show_product_details(digital)
    messages = [
        line for line in details_output.getvalue().splitlines()
        if line.startswith("This product")
    ]

    inventory = Inventory()
    added = [inventory.add_product(physical), inventory.add_product(digital)]
    product_count = len(inventory.get_products())
    inventory_output = io.StringIO()
    with redirect_stdout(inventory_output):
        inventory.display_all()

    stocks = {}
    found_products = {}
    for product_id in ("P001", "D001"):
        product = inventory.find_product(product_id)
        found_products[product_id] = product is not None
        if product is not None:
            product.update_stock(20)
            stocks[product_id] = product.get_stock()

    removed_physical = inventory.remove_product("P001")
    removed_digital = inventory.remove_product("D001")
    expected = {
        "fulfilment_messages": [
            "This product requires physical shipping.",
            "This product is delivered digitally.",
        ],
        "added": [True, True],
        "product_count": 2,
        "both_products_displayed": True,
        "found_products": {"P001": True, "D001": True},
        "updated_stocks": {"P001": 20, "D001": 20},
        "removed_original_objects": [True, True],
        "find_after_removal": [None, None],
        "inventory_empty": True,
    }
    actual = {
        "fulfilment_messages": messages,
        "added": added,
        "product_count": product_count,
        "both_products_displayed": (
            "Laptop" in inventory_output.getvalue()
            and "Software Licence" in inventory_output.getvalue()
        ),
        "found_products": found_products,
        "updated_stocks": stocks,
        "removed_original_objects": [
            removed_physical is physical, removed_digital is digital,
        ],
        "find_after_removal": [
            inventory.find_product("P001"), inventory.find_product("D001"),
        ],
        "inventory_empty": inventory.get_products() == [],
    }
    passed = show_case(
        "PhysicalProduct and DigitalProduct work through Product",
        {"products": ["PhysicalProduct P001", "DigitalProduct D001"],
         "operations": ["display", "add", "find", "update stock", "remove"],
         "new_stock": 20},
        expected,
        actual,
    )
    if not passed:
        raise AssertionError("Product substitution results did not match")


class SubstitutabilityTests(unittest.TestCase):
    def test_product_substitution(self):
        test_substitutability()


if __name__ == "__main__":
    unittest.main(verbosity=0)
