from Classes.discount_strategy import DiscountStrategy
from Classes.discount_none import NoDiscount
from Classes.discount_percentage import PercentageDiscount
from Classes.discount_bulk import BulkDiscount
from Classes.discount_student import StudentDiscount


def create_discount(data: dict | None):
    """Restore saved strategies; Lab 8 orders default to no discount."""
    if data is None:
        return NoDiscount()
    if not isinstance(data, dict):
        raise ValueError("Discount record must be a dictionary")

    discount_type = data.get("type", "none")
    if discount_type == "none":
        return NoDiscount()
    if discount_type == "percentage":
        return PercentageDiscount(float(data["percentage"]))
    if discount_type == "bulk":
        return BulkDiscount(float(data["threshold"]), float(data["amount"]))
    if discount_type == "student":
        return StudentDiscount()
    raise ValueError(f"Unknown discount type: {discount_type}")
