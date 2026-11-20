from .discount_strategy import DiscountStrategy
from .discount_none import NoDiscount
from .product import Product
from .order_line import OrderLine


# =========================================================
# ORDER CLASS (COMPOSITION)
# =========================================================

class Order:
    def __init__(self, order_id: str,
                 discount: DiscountStrategy | None = None) -> None:
        self.__order_id: str = order_id
        self.__order_lines: list[OrderLine] = []
        self.__discount: DiscountStrategy = (
            NoDiscount() if discount is None else discount
        )

    def set_discount(self, discount: DiscountStrategy) -> None:
        self.__discount = discount

    def get_discount(self) -> DiscountStrategy:
        return self.__discount

    def get_order_id(self) -> str:
        return self.__order_id

    def get_order_lines(self) -> tuple[OrderLine, ...]:
        return tuple(self.__order_lines)

    def add_order_line(self, product: Product, quantity: int) -> None:
        # Order creates each OrderLine: the caller only supplies a Product.
        order_line = OrderLine(product, quantity)
        self.__order_lines.append(order_line)

    def remove_order_line(self, product_id: str) -> bool:
        for order_line in self.__order_lines:
            if order_line.get_product().get_product_id() == product_id:
                self.__order_lines.remove(order_line)
                return True

        return False

    def calculate_total(self) -> float:
        total = 0.0

        for order_line in self.__order_lines:
            total += order_line.calculate_subtotal()

        return self.__discount.apply(total)

    def update_order_line(self, line_number: int, quantity: int) -> None:
        if not 1 <= line_number <= len(self.__order_lines):
            raise ValueError("Order line number not found")
        if quantity < 0:
            raise ValueError("Quantity cannot be negative")

        index = line_number - 1
        if quantity == 0:
            self.__order_lines.pop(index)
        else:
            product = self.__order_lines[index].get_product()
            self.__order_lines[index] = OrderLine(product, quantity)

    def display_information(self) -> None:
        print(f"\n===== Order: {self.__order_id} =====")

        for number, order_line in enumerate(self.__order_lines, start=1):
            product = order_line.get_product()
            print(f"{number}. {product.get_product_id()} | {product.get_name()} "
                  f"| Qty: {order_line.get_quantity()} "
                  f"| Subtotal: ${order_line.calculate_subtotal():.2f}")

        print(f"Total: ${self.calculate_total():.2f}")
