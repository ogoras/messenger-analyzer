# Okay, how many ways are there to filter the data?
# 1. sender
#   1a. sender first name
#   1b. sender last name
# 2. timestamp
#   2a. timestamp range
#   2b. days of the week
#   2c. days of the year
#   2d. hours of the day
#   2e. ...
# 3. subfolder (inbox, archived_threads, filtered_threads)
# 4. type (generic, subscribe, unsubscribe, share, call)
#   4a. Generic:
#       4a1. filter by attributes present (content, photos, videos, sticker, audio_files, files, gifs, reactions)
#   4b. ...
# 5. conversation_folder (conversation_id?)
# 6. thread_type (regular, group)
# 7. thread participants

from abc import ABC, abstractmethod
from lib.lexical_processing import match_words

class Filter(ABC):
    @abstractmethod
    def filter(self, subfolder, conversation_folder, thread, message):
        pass

    def negate(self):
        return NegationFilter(self)
    
    def join(self, other, action="and"):
        return CompositeFilter([self, other], action)

class EmptyFilter(Filter):
    def filter(self, subfolder, conversation_folder, thread, message):
        return True

class CompositeFilter(Filter):
    def __init__(self, filters = [], action="and"):
        self.filters = filters
        self.action = action
        if action == "xor" and len(filters != 2):
            raise Exception("XOR filter needs exactly 2 filters")

    def filter(self, subfolder, conversation_folder, thread, message):
        if self.action == "and":
            return all([f.filter(subfolder, conversation_folder, thread, message) for f in self.filters])
        elif self.action == "or":
            return any([f.filter(subfolder, conversation_folder, thread, message) for f in self.filters])
        elif self.action == "xor":
            return (self.filters[0].filter(subfolder, conversation_folder, thread, message) ^ self.filters[1].filter(subfolder, conversation_folder, thread, message))
        else:
            raise Exception("Unknown action: " + self.action)

class NegationFilter(Filter):
    def __init__(self, filter):
        self.inner_filter = filter

    def filter(self, subfolder, conversation_folder, thread, message):
        return not self.inner_filter.filter(subfolder, conversation_folder, thread, message)

class SenderFilter(Filter):
    def __init__(self, sender, match="whole"):
        self.sender = sender
        self.match = match

    def filter(self, subfolder, conversation_folder, thread, message):
        return match_words(self.sender, message["sender_name"])

def senders_filter(senders, match="whole"):
    return CompositeFilter([SenderFilter(sender, match) for sender in senders], "or")

class TypeFilter(Filter):
    def __init__(self, type):
        self.type = type

    def filter(self, subfolder, conversation_folder, thread, message):
        return message["type"] == self.type

class TimeFilter(Filter):
    def __init__(self, time_start, time_end):
        self.time_start = time_start
        self.time_end = time_end
    
    def filter(self, subfolder, conversation_folder, thread, message):
        return self.time_start <= message["timestamp_ms"] <= self.time_end
        