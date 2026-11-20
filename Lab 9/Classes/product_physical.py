from .product import Product
from .supplier import Supplier
from .can_be_shipped import CanBeShipped


# =========================================================
# PHYSICAL PRODUCT CLASS
# =========================================================

class PhysicalProduct(Product, CanBeShipped):
    def __init__(self, product_id: str, name: str, price: float,
                 stock: int, weight: float, supplier: Supplier) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        self.__weight: float = weight

    def get_weight(self) -> float:
        return self.__weight

    def display_information(self) -> None:
        super().display_information()
        print(f"Weight: {self.__weight:.2f} kg")

    def get_fulfilment_info(self) -> str:
        return "This product requires physical shipping."

    def calculate_shipping_cost(self) -> float:
        return self.__weight * 5.00

    def to_dictionary(self) -> dict[str, object]:
        data = super().to_dictionary()
        data["type"] = "physical"
        data["weight"] = self.__weight
        return data
