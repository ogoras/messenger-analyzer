from abc import ABC, abstractmethod

class Categorizer(ABC):
    @abstractmethod
    def categorize(self, subfolder, conversation_folder, thread, message):
        pass

    def __mul__(self, other):
        return MultiCategorizer(self, other)

class EmptyCategorizer(Categorizer):
    def categorize(self, subfolder, conversation_folder, thread, message):
        return None

class UniqueCategorizer(Categorizer):
    def categorize(self, subfolder, conversation_folder, thread, message):
        #calculate hash of all arguments
        return str(hash(subfolder)) + str(hash(conversation_folder)) + str(hash(thread)) + str(hash(message))

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

    def categorize(self, subfolder, conversation_folder, thread, message):
        return self.separator.join([str(categorizer.categorize(subfolder, conversation_folder, thread, message)) for categorizer in self.categorizers])