from math import isfinite
from .discount_strategy import DiscountStrategy


class PercentageDiscount(DiscountStrategy):
    def __init__(self, percentage: float):
        if not isfinite(percentage) or not 0 <= percentage <= 100:
            raise ValueError("Percentage must be between 0 and 100")
        self._percentage: float = percentage

    def apply(self, total: float):
        return total * (1 - self._percentage / 100)
    def to_dictionary(self):
        return {"type": "percentage", "percentage": self._percentage}
