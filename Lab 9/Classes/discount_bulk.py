from math import isfinite
from .discount_strategy import DiscountStrategy


class BulkDiscount(DiscountStrategy):
    def __init__(self, threshold: float, amount: float) -> None:
        if not isfinite(threshold) or threshold < 0:
            raise ValueError("Threshold cannot be negative or non-finite")
        if not isfinite(amount) or amount < 0:
            raise ValueError("Discount amount cannot be negative or non-finite")
        self.__threshold: float = threshold
        self.__amount: float = amount

    def apply(self, total: float) -> float:
        if total >= self.__threshold:
            return max(0.0, total - self.__amount)
        return total

    def to_dictionary(self) -> dict[str, object]:
        return {"type": "bulk", "threshold": self.__threshold,
                "amount": self.__amount}
