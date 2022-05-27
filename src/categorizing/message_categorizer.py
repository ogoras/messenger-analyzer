from .categorizer import Categorizer
from abc import abstractmethod
from ..lib.conversions import decode_fb

class MessageCategorizer(Categorizer):
    def categorize(self, subfolder, conversation_folder, thread, message):
        return self.categorize_message(message)

    @abstractmethod
    def categorize_message(self, message):
        pass

class SenderCategorizer(MessageCategorizer):
    def categorize_message(self, message):
        return decode_fb(message["sender_name"])

class TypeCategorizer(MessageCategorizer):
    def categorize_message(self, message):
        return message["type"]