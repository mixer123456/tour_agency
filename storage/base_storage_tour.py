from abc import ABC, abstractmethod
from schemas import NewTour


class BaseStorageTour(ABC):
    @abstractmethod
    def create_tour(self, new_tour: NewTour):
        pass

    @abstractmethod
    def get_tour(self, _id: int):
        pass

    @abstractmethod
    def get_tours(self, limit: int = 10):
        pass

    @abstractmethod
    def update_tour_price(self, _id: int, new_price: float):
        pass

    @abstractmethod
    def delete_tour(self, _id: int):
        pass
