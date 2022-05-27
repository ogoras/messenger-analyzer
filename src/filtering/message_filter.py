from ..categorizing.message_categorizer import SenderCategorizer
from .filter import Filter, CompositeFilter
from abc import abstractmethod
from .category_filter import MatchFilter

class MessageFilter(Filter):
    def filter(self, subfolder, conversation_folder, thread, message):
        return self.filter_message(message)
    
    @abstractmethod
    def filter_message(self, message):
        pass

# SenderFilter(sender, match) becomes MatchFilter(SenderCategorizer(), sender, match)

def senders_filter(senders, match="whole"):
    return CompositeFilter([MatchFilter(SenderCategorizer(), sender, match) for sender in senders], "or")

# TypeFilter(type) becomes EqualsFilter(TypeCategorizer(), type)

class TimeFilter(MessageFilter):
    def __init__(self, time_start, time_end):
        self.time_start = time_start
        self.time_end = time_end
    
    def filter_message(self, message):
        return self.time_start <= message["timestamp_ms"] <= self.time_end