from abc import ABC, abstractmethod


class OrderStorageInterface(ABC):
    @abstractmethod
    def get_order(self, order_id: str):
        pass

    @abstractmethod
    def get_promo_code_usage(self, promo_code_id: int) -> int:
        pass