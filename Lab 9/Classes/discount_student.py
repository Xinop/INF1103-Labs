from .discount_percentage import PercentageDiscount


class StudentDiscount(PercentageDiscount):
    def __init__(self):
        super().__init__(5)

    def to_dictionary(self):
        return {"type": "student"}
