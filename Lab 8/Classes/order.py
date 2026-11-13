from .product import Product
from .order_line import OrderLine


# =========================================================
# ORDER CLASS (COMPOSITION)
# =========================================================

class Order:
    def __init__(self, order_id: str) -> None:
        self.__order_id: str = order_id
        self.__order_lines: list[OrderLine] = []

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

        return total

    def display_information(self) -> None:
        print(f"\n===== Order: {self.__order_id} =====")

        for order_line in self.__order_lines:
            product = order_line.get_product()
            print(f"{product.get_name()} | Qty: {order_line.get_quantity()} "
                  f"| Subtotal: ${order_line.calculate_subtotal():.2f}")

        print(f"Total: ${self.calculate_total():.2f}")
