from abc import ABC, abstractmethod

class Categorizer(ABC):
    @abstractmethod
    def categorize(self, subfolder, conversation_folder, thread, message):
        pass

class EmptyCategorizer(Categorizer):
    def categorize(self, subfolder, conversation_folder, thread, message):
        return None

class UniqueCategorizer(Categorizer):
    def categorize(self, subfolder, conversation_folder, thread, message):
        #calculate hash of all arguments
        return [hash(subfolder), hash(conversation_folder), hash(thread), hash(message)]

class SubfolderCategorizer(Categorizer):
    def categorize(self, subfolder, conversation_folder, thread, message):
        return subfolder

class ConversationCategorizer(Categorizer):
    def categorize(self, subfolder, conversation_folder, thread, message):
        return conversation_folder