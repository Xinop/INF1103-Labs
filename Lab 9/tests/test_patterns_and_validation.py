"""Report real inputs and results while retaining automated assertions."""

import io
import json
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from Classes.discount_bulk import BulkDiscount
from Classes.discount_none import NoDiscount
from Classes.discount_percentage import PercentageDiscount
from Classes.discount_strategy import DiscountStrategy
from Classes.discount_student import StudentDiscount
from Classes.file_handler_inventory import InventoryFileHandler
from Classes.file_handler_order import OrderFileHandler
from Classes.inventory import Inventory
from Classes.menu import Menu
from Classes.order import Order
from Classes.order_line import OrderLine
from Classes.product import Product
from Classes.product_digital import DigitalProduct
from Classes.product_factory import ProductFactory
from Classes.product_physical import PhysicalProduct
from Classes.product_subscription import SubscriptionProduct
from Classes.supplier import Supplier
from discount_types import create_discount
from load_products import load_products
from menu_functions import add_product, get_positive_float, update_order
from product_types import create_product
from tests.reporting import capture_value_error, show_case
from tests.test_substitutability import show_product_details


ROOT = Path(__file__).resolve().parents[1]


class BaseTestCase(unittest.TestCase):
    """Shared fixtures and one consistent reporting format."""

    def setUp(self):
        self.supplier = Supplier("S001", "Lab Supplier", "lab@example.com")

    def product(
        self, product_type="physical", price=125.0, stock=10, **extras
    ):
        return ProductFactory.create(
            product_type, "P001", "Example", price, stock,
            self.supplier, **extras,
        )

    def order(self, strategy=None):
        order = Order("O001", strategy)
        order.add_order_line(self.product(), 2)
        return order

    def check_case(self, name, test_input, expected, actual):
        show_case(name, test_input, expected, actual)
        self.assertEqual(actual, expected)


class DiscountTests(BaseTestCase):
    def test_default_is_no_discount(self):
        order = self.order()
        actual = {
            "strategy": type(order.get_discount()).__name__,
            "total": order.calculate_total(),
        }
        self.check_case(
            "Default order uses NoDiscount",
            {"price": 125.0, "quantity": 2, "discount": None},
            {"strategy": "NoDiscount", "total": 250.0},
            actual,
        )

    def test_strategy_can_change_on_same_order(self):
        order = self.order(BulkDiscount(200, 20))
        totals = [order.calculate_total()]
        order.set_discount(PercentageDiscount(10))
        totals.append(order.calculate_total())
        order.set_discount(StudentDiscount())
        totals.append(order.calculate_total())
        self.check_case(
            "Change discount on the same order",
            {"subtotal": 250, "strategies": [
                "BulkDiscount(200, 20)", "PercentageDiscount(10)",
                "StudentDiscount()",
            ]},
            [230.0, 225.0, 237.5],
            totals,
        )

    def test_bulk_threshold_boundaries(self):
        strategy = BulkDiscount(200, 20)
        actual = [strategy.apply(total) for total in (199, 200, 250)]
        actual.append(BulkDiscount(0, 20).apply(10))
        self.check_case(
            "Bulk discount threshold and minimum total",
            ["(200, 20) on 199", "(200, 20) on 200",
             "(200, 20) on 250", "(0, 20) on 10"],
            [199, 180, 230, 0],
            actual,
        )

    def test_percentage_boundaries(self):
        self.check_case(
            "Percentage discount at 0% and 100%",
            {"total": 250, "percentages": [0, 100]},
            [250, 0],
            [PercentageDiscount(0).apply(250),
             PercentageDiscount(100).apply(250)],
        )

    def test_invalid_discount_configuration(self):
        percentages = (-1, 101, float("nan"), float("inf"))
        actual = [capture_value_error(
            lambda value=value: PercentageDiscount(value)
        ) for value in percentages]
        actual.extend([
            capture_value_error(lambda: BulkDiscount(-1, 20)),
            capture_value_error(lambda: BulkDiscount(200, -1)),
        ])
        expected = [
            "ValueError: Percentage must be between 0 and 100"
        ] * 4 + [
            "ValueError: Threshold cannot be negative or non-finite",
            "ValueError: Discount amount cannot be negative or non-finite",
        ]
        self.check_case(
            "Reject invalid discount settings",
            {"percentages": percentages, "bulk": [(-1, 20), (200, -1)]},
            expected,
            actual,
        )

    def test_new_strategy_needs_no_order_changes(self):
        class FixedFiveDiscount(DiscountStrategy):
            def apply(self, total: float):
                return max(0.0, total - 5)

        self.check_case(
            "Use a new strategy without changing Order",
            {"subtotal": 250, "strategy": "FixedFiveDiscount"},
            245,
            self.order(FixedFiveDiscount()).calculate_total(),
        )

    def test_two_orders_can_share_strategy(self):
        strategy = PercentageDiscount(10)
        first = self.order(strategy)
        second = self.order(strategy)
        self.check_case(
            "Two orders share one discount strategy",
            {"subtotal_per_order": 250, "shared_discount": "10%"},
            {"same_strategy_object": True, "totals": [225, 225]},
            {"same_strategy_object": (
                first.get_discount() is second.get_discount()
            ), "totals": [first.calculate_total(), second.calculate_total()]},
        )

    def test_empty_order_total(self):
        self.check_case(
            "An empty order cannot have a negative total",
            {"lines": [], "discount": "BulkDiscount(0, 20)"},
            0,
            Order("O002", BulkDiscount(0, 20)).calculate_total(),
        )


class FactoryAndValidationTests(BaseTestCase):
    def test_factory_returns_supported_product_types(self):
        actual = []
        for kind in ("physical", "digital", "subscription"):
            product = self.product(kind)
            actual.append({
                "class": type(product).__name__,
                "is_product": isinstance(product, Product),
                "same_supplier": product.get_supplier() is self.supplier,
            })
        expected = [{
            "class": name, "is_product": True, "same_supplier": True
        } for name in (
            "PhysicalProduct", "DigitalProduct", "SubscriptionProduct"
        )]
        self.check_case(
            "Factory creates the correct Product subclasses",
            ["physical", "digital", "subscription"], expected, actual,
        )

    def test_factory_keeps_subtype_fields(self):
        self.check_case(
            "Factory preserves specialised product fields",
            {"weight": 2.5, "download_size": 850, "duration_months": 12},
            {"weight": 2.5, "download_size": 850, "duration_months": 12},
            {
                "weight": self.product(weight=2.5).get_weight(),
                "download_size": self.product(
                    "digital", download_size=850
                ).get_download_size(),
                "duration_months": self.product(
                    "subscription", duration_months=12
                ).get_duration_months(),
            },
        )

    def test_unknown_type_raises_clear_error(self):
        self.check_case(
            "Factory rejects an unknown product type",
            {"product_type": "service"},
            "ValueError: Unknown product type: service",
            capture_value_error(lambda: self.product("service")),
        )

    def test_base_class_validates_direct_subclass_construction(self):
        self.check_case(
            "Validation still works when the factory is bypassed",
            {"physical_price": 0, "digital_stock": -1},
            ["ValueError: Price must be greater than zero and finite",
             "ValueError: Stock cannot be negative"],
            [
                capture_value_error(lambda: PhysicalProduct(
                    "P1", "Invalid", 0, 1, 1, self.supplier
                )),
                capture_value_error(lambda: DigitalProduct(
                    "D1", "Invalid", 10, -1, 1, self.supplier
                )),
            ],
        )

    def test_all_subclasses_reject_invalid_prices(self):
        kinds = ("physical", "digital", "subscription")
        prices = (0, -5, float("nan"), float("inf"))
        actual = []
        for kind in kinds:
            actual.extend(capture_value_error(
                lambda price=price: self.product(kind, price=price)
            ) for price in prices)
        self.check_case(
            "Every Product subclass rejects invalid prices",
            {"types": kinds, "prices_for_each_type": prices},
            ["ValueError: Price must be greater than zero and finite"] * 12,
            actual,
        )

    def test_stock_rule_preserved_by_subclasses(self):
        actual = []
        for kind in ("physical", "digital", "subscription"):
            invalid_initial_stock = capture_value_error(
                lambda: self.product(kind, stock=-1)
            )
            product = self.product(kind, stock=0)
            product.update_stock(5)
            invalid_update = capture_value_error(
                lambda: product.update_stock(-1)
            )
            actual.append({
                "initial_stock_error": invalid_initial_stock,
                "update_error": invalid_update,
                "stock_after_failed_update": product.get_stock(),
            })
        expected = [{
            "initial_stock_error": "ValueError: Stock cannot be negative",
            "update_error": "ValueError: Stock cannot be negative",
            "stock_after_failed_update": 5,
        }] * 3
        self.check_case(
            "All subclasses preserve the stock rule",
            {"types": ["physical", "digital", "subscription"],
             "initial_invalid_stock": -1, "updates": [5, -1]},
            expected, actual,
        )

    def test_invalid_order_line_quantity_rejected(self):
        errors = [capture_value_error(
            lambda quantity=quantity: OrderLine(self.product(), quantity)
        ) for quantity in (0, -1)]
        order = self.order()
        errors.append(capture_value_error(
            lambda: order.update_order_line(1, -1)
        ))
        total_after_error = order.calculate_total()
        order.update_order_line(1, 0)
        self.check_case(
            "Reject invalid quantities and allow explicit line removal",
            {"new_line_quantities": [0, -1], "updates": [-1, 0]},
            {"errors": [
                "ValueError: Order quantity must be positive",
                "ValueError: Order quantity must be positive",
                "ValueError: Quantity cannot be negative",
            ], "total_after_failed_update": 250, "remaining_lines": 0},
            {"errors": errors, "total_after_failed_update": total_after_error,
             "remaining_lines": len(order.get_order_lines())},
        )

    def test_common_product_function_is_polymorphic(self):
        products = [self.product(), self.product("digital")]
        output = io.StringIO()
        with redirect_stdout(output):
            for product in products:
                show_product_details(product)
        messages = [line for line in output.getvalue().splitlines()
                    if line.startswith("This product")]
        self.check_case(
            "One Product function uses both subclass implementations",
            "Pass a PhysicalProduct and DigitalProduct to the same function",
            ["This product requires physical shipping.",
             "This product is delivered digitally."],
            messages,
        )

    def test_json_adapter_uses_factory(self):
        record = self.product("digital", download_size=5).to_dictionary()
        with patch(
            "product_types.ProductFactory.create", wraps=ProductFactory.create
        ) as factory:
            product = create_product(record, self.supplier)
        self.check_case(
            "JSON product loading uses the factory",
            record,
            {"factory_calls": 1, "download_size": 5},
            {"factory_calls": factory.call_count,
             "download_size": product.get_download_size()},
        )


class InputAndCSVTests(BaseTestCase):
    def test_price_reprompts_and_returns_valid_float(self):
        answers = ["abc", "-5", "12.50"]
        output = io.StringIO()
        with patch("builtins.input", side_effect=answers):
            with redirect_stdout(output):
                value = get_positive_float("Price: ")
        self.check_case(
            "Price input retries until a valid value is entered",
            answers,
            {"returned_price": 12.5, "messages": [
                "Please enter a valid number, e.g. 12.50",
                "Please enter a number greater than zero.",
            ]},
            {"returned_price": value,
             "messages": output.getvalue().splitlines()},
        )

    def test_price_rejects_zero_and_nonfinite_values(self):
        answers = ["0", "nan", "inf", "1"]
        output = io.StringIO()
        with patch("builtins.input", side_effect=answers):
            with redirect_stdout(output):
                value = get_positive_float("Price: ")
        self.check_case(
            "Price input rejects zero, NaN, and infinity",
            answers,
            {"returned_price": 1, "rejection_messages": 3},
            {"returned_price": value,
             "rejection_messages": len(output.getvalue().splitlines())},
        )

    def test_sample_csv_loads_three_products_and_skips_bad_rows(self):
        inventory = Inventory()
        output = io.StringIO()
        with redirect_stdout(output):
            load_products(str(ROOT / "products.csv"), inventory, self.supplier)
        self.check_case(
            "CSV loads valid products and skips invalid rows",
            (ROOT / "products.csv").read_text(),
            {"product_ids": ["P001", "D001", "P003"], "messages": [
                "Skipping row 4: Unknown product type: service",
                "Skipping row 5: could not convert string to float: 'abc'",
                "3 products loaded.", "Load attempt finished.",
            ]},
            {"product_ids": [p.get_product_id()
                             for p in inventory.get_products()],
             "messages": output.getvalue().splitlines()},
        )

    def test_missing_csv_runs_except_and_finally(self):
        output = io.StringIO()
        with TemporaryDirectory() as directory:
            missing = str(Path(directory) / "missing.csv")
            with redirect_stdout(output):
                load_products(missing, Inventory(), self.supplier)
        self.check_case(
            "A missing CSV is handled without crashing",
            {"path": missing, "file_exists": False},
            [f"Products file not found: {missing}", "Load attempt finished."],
            output.getvalue().splitlines(),
        )

    def test_bad_rows_and_duplicate_ids_do_not_stop_import(self):
        csv_data = (
            "product_type,product_id,name,price,stock_quantity\n"
            "physical,P1,Bad Price,0,1\n"
            "digital,D1,Bad Stock,5,-1\n"
            "physical,P2,Valid,10,2\n"
            "physical,P2,Duplicate,10,2\n"
            "too,few,columns\n"
            "digital,D2,Later Valid,20,2\n"
        )
        with TemporaryDirectory() as directory:
            path = Path(directory) / "products.csv"
            path.write_text(csv_data)
            inventory = Inventory()
            with redirect_stdout(io.StringIO()):
                load_products(str(path), inventory, self.supplier)
        self.check_case(
            "Bad rows and duplicate IDs do not stop later valid rows",
            csv_data,
            ["P2", "D2"],
            [product.get_product_id() for product in inventory.get_products()],
        )

    def test_empty_csv_still_finishes(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "empty.csv"
            path.write_text("")
            output = io.StringIO()
            with redirect_stdout(output):
                load_products(str(path), Inventory(), self.supplier)
        self.check_case(
            "An empty CSV finishes with zero loaded products",
            "An empty CSV file",
            ["0 products loaded.", "Load attempt finished."],
            output.getvalue().splitlines(),
        )

    def test_menu_add_product_uses_factory_and_price_helper(self):
        inventory = Inventory()
        answers = ["Lamp", "abc", "-5", "12.50", "3", "1", "1.5",
                   "4", "Supplier", "supplier@example.com"]
        with patch("builtins.input", side_effect=answers):
            with redirect_stdout(io.StringIO()):
                with patch("menu_functions.ProductFactory.create",
                           wraps=ProductFactory.create) as factory:
                    add_product(inventory)
        product = inventory.find_product("P001")
        actual = {"factory_calls": factory.call_count, "product": None}
        if product is not None:
            actual["product"] = {
                "id": product.get_product_id(), "price": product.get_price(),
                "supplier_id": product.get_supplier().get_supplier_id(),
            }
        self.check_case(
            "Add Product validates price and calls the factory",
            answers,
            {"factory_calls": 1, "product": {
                "id": "P001", "price": 12.5, "supplier_id": "S001",
            }},
            actual,
        )


class PersistenceAndMenuTests(BaseTestCase):
    def test_each_discount_survives_saved_order(self):
        strategies = (NoDiscount(), PercentageDiscount(10),
                      BulkDiscount(200, 20), StudentDiscount())
        actual = []
        with TemporaryDirectory() as directory:
            handler = OrderFileHandler(str(Path(directory) / "orders.json"))
            for strategy in strategies:
                order = self.order(strategy)
                with redirect_stdout(io.StringIO()):
                    handler.save_orders([order])
                restored = handler.load_orders(Inventory())[0]
                actual.append({
                    "strategy": type(restored.get_discount()).__name__,
                    "total": restored.calculate_total(),
                })
        self.check_case(
            "Saved orders restore every discount strategy",
            {"subtotal": 250, "strategies": [
                "NoDiscount", "PercentageDiscount(10)",
                "BulkDiscount(200, 20)", "StudentDiscount",
            ]},
            [
                {"strategy": "NoDiscount", "total": 250},
                {"strategy": "PercentageDiscount", "total": 225},
                {"strategy": "BulkDiscount", "total": 230},
                {"strategy": "StudentDiscount", "total": 237.5},
            ],
            actual,
        )

    def test_legacy_order_defaults_to_no_discount(self):
        record = {"order_id": "O001", "order_lines": [
            {"product": self.product().to_dictionary(), "quantity": 2}
        ]}
        with TemporaryDirectory() as directory:
            path = Path(directory) / "orders.json"
            path.write_text(json.dumps([record]))
            restored = OrderFileHandler(str(path)).load_orders(Inventory())[0]
        self.check_case(
            "An older order without discount data uses NoDiscount",
            {"order_id": "O001", "subtotal": 250,
             "discount_field_present": False},
            {"strategy": "NoDiscount", "total": 250},
            {"strategy": type(restored.get_discount()).__name__,
             "total": restored.calculate_total()},
        )

    def test_saved_order_reuses_inventory_product(self):
        inventory = Inventory()
        product = self.product()
        inventory.add_product(product)
        order = Order("O001", PercentageDiscount(10))
        order.add_order_line(product, 2)
        with TemporaryDirectory() as directory:
            handler = OrderFileHandler(str(Path(directory) / "orders.json"))
            with redirect_stdout(io.StringIO()):
                handler.save_orders([order])
            restored = handler.load_orders(inventory)[0]
        self.check_case(
            "An order reload reuses its inventory Product object",
            {"product_id": "P001", "quantity": 2, "discount": "10%"},
            {"same_product_object": True, "total": 225},
            {"same_product_object": (
                restored.get_order_lines()[0].get_product() is product
            ), "total": restored.calculate_total()},
        )

    def test_create_order_menu_saves_discount_and_keeps_exit_number(self):
        answers = ["7", "P001", "2", "", "2", "10", "10"]
        with TemporaryDirectory() as directory:
            inventory = Inventory()
            inventory.add_product(self.product())
            inventory_handler = InventoryFileHandler(
                str(Path(directory) / "inventory.json")
            )
            order_handler = OrderFileHandler(
                str(Path(directory) / "orders.json")
            )
            menu = Menu(inventory, inventory_handler, order_handler)
            with patch("builtins.input", side_effect=answers):
                with redirect_stdout(io.StringIO()):
                    menu.run()
            restored_inventory = inventory_handler.load_inventory()
            restored = order_handler.load_orders(restored_inventory)[0]
        self.check_case(
            "Create Order saves its discount and option 10 exits",
            {"menu_inputs": answers, "meaning":
             "Create order, add 2 products, choose 10%, then exit"},
            {"order_id": "O001", "saved_total": 225},
            {"order_id": restored.get_order_id(),
             "saved_total": restored.calculate_total()},
        )

    def test_existing_order_discount_can_change_from_update_menu(self):
        order = self.order()
        answers = ["O001", "d", "4", ""]
        with patch("builtins.input", side_effect=answers):
            with redirect_stdout(io.StringIO()):
                changed = update_order([order], Inventory())
        self.check_case(
            "Update Order changes the discount to StudentDiscount",
            {"menu_inputs": answers, "subtotal": 250},
            {"changed": True, "total": 237.5},
            {"changed": changed, "total": order.calculate_total()},
        )

    def test_unknown_saved_discount_raises_clear_error(self):
        self.check_case(
            "Reject an unknown saved discount type",
            {"type": "unknown"},
            "ValueError: Unknown discount type: unknown",
            capture_value_error(lambda: create_discount({"type": "unknown"})),
        )


if __name__ == "__main__":
    unittest.main(verbosity=0)
