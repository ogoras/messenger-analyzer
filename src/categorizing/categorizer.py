from abc import ABC, abstractmethod
from ast import arg

class Categorizer(ABC):
    @abstractmethod
    def categorize(self, *args):
        pass

    def __mul__(self, other):
        return MultiCategorizer(self, other)

class EmptyCategorizer(Categorizer):
    def categorize(self, *args):
        return None

class UniqueCategorizer(Categorizer):
    def categorize(self, *args):
        #calculate hash of all arguments
        return "".join([str(hash(arg)) for arg in args])

class SubfolderCategorizer(Categorizer):
    def categorize(self, subfolder, conversation_folder, thread, message):
        return subfolder

class ConversationCategorizer(Categorizer):
    def categorize(self, subfolder, conversation_folder, thread, message):
        return conversation_folder

class MultiCategorizer(Categorizer):
    def __init__(self, *categorizers, separator = " "):
        self.categorizers = categorizers
        self.separator = separator

    def categorize(self, *args):
        return self.separator.join([str(categorizer.categorize(*args)) for categorizer in self.categorizers])