from .product import Product


# =========================================================
# ORDER LINE CLASS (OWNED BY ORDER)
# =========================================================

class OrderLine:
    def __init__(self, product: Product, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError("Order quantity must be positive")

        self.__product: Product = product
        self.__quantity: int = quantity

    def get_product(self) -> Product:
        return self.__product

    def get_quantity(self) -> int:
        return self.__quantity

    def calculate_subtotal(self) -> float:
        return self.__product.get_price() * self.__quantity
