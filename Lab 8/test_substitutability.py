from Classes.inventory import Inventory
from Classes.product import Product
from Classes.product_digital import DigitalProduct
from Classes.product_physical import PhysicalProduct
from Classes.supplier import Supplier


def show_product_details(product: Product) -> None:
    """Use the same Product operations for either subclass."""
    product.display_information()
    print(product.get_fulfilment_info())


def test_substitutability() -> None:
    supplier = Supplier("S001", "Tech Supplier", "sales@example.com")
    physical = PhysicalProduct("P001", "Laptop", 1200.0, 5, 2.5, supplier)
    digital = DigitalProduct("D001", "Software Licence", 50.0, 10, 850.0, supplier)

    print("=== Same function, two Product subclasses ===")
    show_product_details(physical)
    show_product_details(digital)

    print("\n=== Both subclasses in the same Inventory ===")
    inventory = Inventory()
    assert inventory.add_product(physical)
    assert inventory.add_product(digital)
    assert len(inventory.get_products()) == 2
    inventory.display_all()

    # find and update either product through the common Product interface
    for product_id in ("P001", "D001"):
        product = inventory.find_product(product_id)
        assert product is not None
        product.update_stock(20)
        assert product.get_stock() == 20
        show_product_details(product)

    assert inventory.remove_product("P001") is physical
    assert inventory.remove_product("D001") is digital
    assert inventory.find_product("P001") is None
    assert inventory.find_product("D001") is None
    assert inventory.get_products() == []

    print("\nSection 6.2 passed: both subclasses support the same Product operations.")


if __name__ == "__main__":
    test_substitutability()
