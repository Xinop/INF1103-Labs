from .product import Product


# =========================================================
# INVENTORY CLASS (AGGREGATION)
# =========================================================

class Inventory:
    def __init__(self) -> None:
        self.__products: list[Product] = []

    def add_product(self, product: Product) -> bool:
        if self.find_product(product.get_product_id()) is not None:
            return False

        self.__products.append(product)
        return True

    def find_product(self, product_id: str) -> Product | None:
        for product in self.__products:
            if product.get_product_id().lower() == product_id.lower():
                return product

        return None

    # Retain the old method name for the existing menu.
    def search_product(self, product_id: str) -> Product | None:
        return self.find_product(product_id)

    def remove_product(self, product_id: str) -> Product | None:
        product = self.find_product(product_id)

        if product is not None:
            self.__products.remove(product)

        return product

    def display_all(self) -> None:
        print("\nCurrent Inventory")
        print("------------------------------------------")

        if len(self.__products) == 0:
            print("(No products found)")
            print("------------------------------------------")
            return

        for product in self.__products:
            product.display_information()

        print("------------------------------------------")

    def get_products(self) -> list[Product]:
        return self.__products
