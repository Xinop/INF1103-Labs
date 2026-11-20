from .discount_strategy import DiscountStrategy


class NoDiscount(DiscountStrategy):
    def apply(self, total: float) -> float:
        return total

    def to_dictionary(self) -> dict[str, object]:
        return {"type": "none"}
