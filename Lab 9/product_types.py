from Classes.product_physical import PhysicalProduct
from Classes.product_digital import DigitalProduct
from Classes.product_subscription import SubscriptionProduct
from Classes.product import Product
from Classes.supplier import Supplier


# =========================================================
# PRODUCT TYPE REGISTRY
# Add new types here without changing Product, Inventory,
# the file handlers, or Menu.
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


def create_product(data: dict, supplier: Supplier) -> Product:
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
        extra_value,
        supplier
    )


def restore_supplier(data: dict, suppliers: dict[str, Supplier]) -> Supplier:
    supplier_data = data.get("supplier")

    if supplier_data is None:
        # Legacy files contain no supplier information.
        supplier_data = {
            "supplier_id": "UNASSIGNED",
            "name": "Unassigned (legacy product)",
            "contact_email": ""
        }

    supplier_id = supplier_data["supplier_id"]
    supplier_key = supplier_id.lower()
    supplier = suppliers.get(supplier_key)

    if supplier is None:
        supplier = Supplier(
            supplier_id,
            supplier_data["name"],
            supplier_data["contact_email"]
        )
        suppliers[supplier_key] = supplier

    return supplier

