from .product import Product
from .supplier import Supplier


# =========================================================
# DIGITAL PRODUCT CLASS
# =========================================================

class DigitalProduct(Product):
    def __init__(self, product_id: str, name: str, price: float,
                 stock: int, download_size: float, supplier: Supplier) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        self.__download_size: float = download_size

    def get_download_size(self) -> float:
        return self.__download_size

    def display_information(self) -> None:
        super().display_information()
        print(f"Download Size: {self.__download_size:.2f} MB")

    def get_fulfilment_info(self) -> str:
        return "This product is delivered digitally."

    def to_dictionary(self) -> dict[str, object]:
        data = super().to_dictionary()
        data["type"] = "digital"
        data["download_size"] = self.__download_size
        return data
