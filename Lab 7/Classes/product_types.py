from .product_physical import PhysicalProduct
from .product_digital import DigitalProduct
from .product_subscription import SubscriptionProduct


# =========================================================
# PRODUCT TYPE REGISTRY
# Add new types here without changing Product, Inventory,
# FileHandler, or Menu.
# =========================================================

PRODUCT_TYPES = {
    "physical": {
        "option": "1",
        "label": "Physical Product",
        "class": PhysicalProduct,
        "field": "weight",
        "prompt": "Weight (kg): ",
        "convert": float,
        "minimum": 0,
        "default": 0
    },
    "digital": {
        "option": "2",
        "label": "Digital Product",
        "class": DigitalProduct,
        "field": "download_size",
        "prompt": "Download Size (MB): ",
        "convert": float,
        "minimum": 0,
        "default": None
    },
    "subscription": {
        "option": "3",
        "label": "Subscription Product",
        "class": SubscriptionProduct,
        "field": "duration_months",
        "prompt": "Duration (months): ",
        "convert": int,
        "minimum": 1,
        "default": None
    }
}


def create_product(data):
    if not isinstance(data, dict):
        raise ValueError("Inventory record must be a dictionary")

    product_type = data.get("type", "physical")
    product_info = PRODUCT_TYPES.get(product_type)

    if product_info is None:
        raise ValueError(f"Unknown product type: {product_type}")

    extra_value = data.get(product_info["field"], product_info["default"])
    if extra_value is None:
        raise ValueError(f"Missing {product_info['field']}")

    extra_value = product_info["convert"](extra_value)
    if extra_value < product_info["minimum"]:
        raise ValueError(f"Invalid {product_info['field']}")

    return product_info["class"](
        data["id"],
        data["name"],
        float(data["price"]),
        int(data["stock"]),
        extra_value
    )
