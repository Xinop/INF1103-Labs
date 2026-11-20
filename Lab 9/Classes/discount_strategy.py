from abc import ABC, abstractmethod


class DiscountStrategy(ABC):
    @abstractmethod
    def apply(self, total: float):
        pass

    def to_dictionary(self):
        raise ValueError("This discount strategy does not support saving")
