from .product import Product


# =========================================================
# SUBSCRIPTION PRODUCT CLASS (OPTIONAL LAB 7 CHALLENGE)
# =========================================================

class SubscriptionProduct(Product):
    def __init__(self, product_id, name, price, stock, duration_months):
        super().__init__(product_id, name, price, stock)
        self.__duration_months = duration_months

    def get_duration_months(self):
        return self.__duration_months

    def display_information(self):
        super().display_information()
        print(f"Duration: {self.__duration_months} month(s)")

    def get_fulfilment_info(self):
        return "This subscription is activated digitally."

    def to_dictionary(self):
        data = super().to_dictionary()
        data["type"] = "subscription"
        data["duration_months"] = self.__duration_months
        return data
