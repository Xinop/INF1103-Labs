from .product import Product
from .supplier import Supplier


# =========================================================
# SUBSCRIPTION PRODUCT CLASS
# =========================================================

class SubscriptionProduct(Product):
    def __init__(self, product_id: str, name: str, price: float,
                 stock: int, duration_months: int, supplier: Supplier) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        self.__duration_months: int = duration_months

    def get_duration_months(self) -> int:
        return self.__duration_months

    def display_information(self) -> None:
        super().display_information()
        print(f"Duration: {self.__duration_months} month(s)")

    def get_fulfilment_info(self) -> str:
        return "This subscription is activated digitally."

    def to_dictionary(self) -> dict[str, object]:
        data = super().to_dictionary()
        data["type"] = "subscription"
        data["duration_months"] = self.__duration_months
        return data
