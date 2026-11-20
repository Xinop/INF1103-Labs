from .product import Product
from .product_physical import PhysicalProduct
from .product_digital import DigitalProduct
from .product_subscription import SubscriptionProduct
from .supplier import Supplier


class ProductFactory:
    @staticmethod
    def create(product_type: str, product_id: str, name: str, price: float,
               stock_quantity: int, supplier: Supplier, weight: float = 0.0,
               download_size: float = 0.0,
               duration_months: int = 1):
        # The lab CSV omits subtype fields, so simple defaults are provided.
        if product_type == "physical":
            if weight < 0:
                raise ValueError("Weight cannot be negative")
            return PhysicalProduct(product_id, name, price, stock_quantity,
                                   weight, supplier)
        if product_type == "digital":
            if download_size < 0:
                raise ValueError("Download size cannot be negative")
            return DigitalProduct(product_id, name, price, stock_quantity,
                                  download_size, supplier)
        if product_type == "subscription":
            if duration_months < 1:
                raise ValueError("Duration must be at least one month")
            return SubscriptionProduct(product_id, name, price, stock_quantity,
                                       duration_months, supplier)
        raise ValueError(f"Unknown product type: {product_type}")
