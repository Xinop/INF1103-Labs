from .product import Product


# =========================================================
# ORDER LINE CLASS (OWNED BY ORDER)
# =========================================================

class OrderLine:
    def __init__(self, product: Product, quantity: int):
        if quantity <= 0:
            raise ValueError("Order quantity must be positive")

        self._product: Product = product
        self._quantity: int = quantity

    def get_product(self):
        return self._product

    def get_quantity(self):
        return self._quantity

    def calculate_subtotal(self):
        return self._product.get_price() * self._quantity
