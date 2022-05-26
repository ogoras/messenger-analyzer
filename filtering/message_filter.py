from filtering.filter import Filter, CompositeFilter
from abc import abstractmethod
from lib.lexical_processing import match_words

class MessageFilter(Filter):
    def filter(self, subfolder, conversation_folder, thread, message):
        return self.filter_message(message)
    
    @abstractmethod
    def filter_message(self, message):
        pass

class SenderFilter(MessageFilter):
    def __init__(self, sender, match="whole"):
        self.sender = sender
        self.match = match

    def filter_message(self, message):
        return match_words(self.sender, message["sender_name"])

def senders_filter(senders, match="whole"):
    return CompositeFilter([SenderFilter(sender, match) for sender in senders], "or")

class TypeFilter(MessageFilter):
    def __init__(self, type):
        self.type = type

    def filter_message(self, message):
        return message["type"] == self.type

class TimeFilter(MessageFilter):
    def __init__(self, time_start, time_end):
        self.time_start = time_start
        self.time_end = time_end
    
    def filter_messag(self, message):
        return self.time_start <= message["timestamp_ms"] <= self.time_end