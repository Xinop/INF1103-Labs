from abc import ABC, abstractmethod


# =========================================================
# CAN BE SHIPPED INTERFACE
# =========================================================

class CanBeShipped(ABC):
    @abstractmethod
    def calculate_shipping_cost(self):
        pass
