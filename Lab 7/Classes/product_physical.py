from .product import Product
from .can_be_shipped import CanBeShipped


# =========================================================
# PHYSICAL PRODUCT CLASS
# =========================================================

class PhysicalProduct(Product, CanBeShipped):
    def __init__(self, product_id, name, price, stock, weight):
        super().__init__(product_id, name, price, stock)
        self.__weight = weight

    def get_weight(self):
        return self.__weight

    def display_information(self):
        super().display_information()
        print(f"Weight: {self.__weight:.2f} kg")

    def get_fulfilment_info(self):
        return "This product requires physical shipping."

    def calculate_shipping_cost(self):
        return self.__weight * 5.00

    def to_dictionary(self):
        data = super().to_dictionary()
        data["type"] = "physical"
        data["weight"] = self.__weight
        return data
