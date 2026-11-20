from abc import ABC, abstractmethod


class DiscountStrategy(ABC):
    @abstractmethod
    def apply(self, total: float) -> float:
        pass

    def to_dictionary(self) -> dict[str, object]:
        raise ValueError("This discount strategy does not support saving")
