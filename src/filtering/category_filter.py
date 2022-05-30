from ..categorizing.categorizer import Categorizer
from .filter import Filter
from abc import abstractmethod
from ..lib.lexical_processing import match_words

class CategoryFilter(Filter):
    def __init__(self, categorizer : Categorizer):
        self.categorizer = categorizer

    def filter(self, *args):
        return self.filter_category(self.categorizer.categorize(*args))

    @abstractmethod
    def filter_category(self, category):
        pass

class EqualsFilter(CategoryFilter):
    def __init__(self, categorizer, category):
        super().__init__(categorizer)
        self.category = category

    def filter_category(self, category):
        return category == self.category

class ContainsFilter(CategoryFilter):
    def __init__(self, categorizer, categories):
        super().__init__(categorizer)
        self.categories = categories

    def filter_category(self, category):
        return category in self.categories

class RangeFilter(CategoryFilter):
    def __init__(self, categorizer, category_start, category_end):
        super().__init__(categorizer)
        self.category_start = category_start
        self.category_end = category_end

    def filter_category(self, category):
        return self.category_start <= category <= self.category_end

class MatchFilter(CategoryFilter):
    def __init__(self, categorizer, pattern, match="whole"):
        super().__init__(categorizer)
        self.match = match
        self.pattern = pattern

    def filter_category(self, category):
        return match_words(self.pattern, category)