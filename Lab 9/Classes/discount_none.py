from .discount_strategy import DiscountStrategy

class NoDiscount(DiscountStrategy):
    def apply(self, total: float):
        return total

    def to_dictionary(self):
        return {"type": "none"}
