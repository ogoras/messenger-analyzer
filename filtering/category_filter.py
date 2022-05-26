from filtering.filter import Filter, CompositeFilter
from abc import abstractmethod

class CategoryFilter(Filter):
    def __init__(self, categorizer):
        self.categorizer = categorizer

    def filter(self, subfolder, conversation_folder, thread, message):
        return self.filter_category(self.categorizer.categorize(subfolder, conversation_folder, thread, message))

    @abstractmethod
    def filter_category(self, category):
        pass

class EqualsFilter(CategoryFilter):
    def __init__(self, categorizer, category):
        super().__init__(categorizer)
        self.category = category

    def filter_category(self, category):
        return category == self.category