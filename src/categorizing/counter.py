from abc import abstractmethod
from .categorizer import Categorizer

class Counter(Categorizer):
    @abstractmethod
    def categorize(self, *args) -> int:
        pass