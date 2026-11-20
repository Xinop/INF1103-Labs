from math import isfinite
from abc import ABC, abstractmethod
from .supplier import Supplier


# =========================================================
# PRODUCT CLASS
# =========================================================

class Product(ABC):
    def __init__(self, product_id: str, name: str, price: float,
                 stock: int, supplier: Supplier):
        if not isfinite(price) or price <= 0:
            raise ValueError("Price must be greater than zero and finite")
        if stock < 0:
            raise ValueError("Stock cannot be negative")

        self.__product_id: str = product_id
        self.__name: str = name
        self.__price: float = price
        self.__stock: int = stock
        self.__supplier: Supplier = supplier

    def get_product_id(self):
        return self.__product_id

    def get_name(self):
        return self.__name

    def get_price(self):
        return self.__price

    def get_stock(self):
        return self.__stock

    def get_supplier(self):
        return self.__supplier

    def update_stock(self, quantity: int):
        if quantity < 0:
            raise ValueError("Stock cannot be negative")
        self.__stock = quantity

    def display_supplier_information(self):
        self.__supplier.display_information()

    def display_information(self):
        print(
            f"ID: {self.__product_id} | "
            f"Name: {self.__name} | "
            f"Price: ${self.__price:.2f} | "
            f"Stock: {self.__stock}"
        )
        print(f"Supplier: {self.__supplier.get_name()} "
              f"({self.__supplier.get_supplier_id()})")

    def to_dictionary(self):
        return {
            "id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
            "supplier": self.__supplier.to_dictionary()
        }

    @abstractmethod
    def get_fulfilment_info(self):
        pass
