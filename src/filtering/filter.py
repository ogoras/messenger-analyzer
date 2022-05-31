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

class Filter(ABC):
    @abstractmethod
    def filter(self, *args) -> bool:
        pass

    def __invert__(self):
        return NegationFilter(self)
    
    def __and__(self, other):
        if not isinstance(other, Filter):
            raise TypeError("Can only combine filters")
        return CompositeFilter([self, other], "and")

    def __or__(self, other):
        if not isinstance(other, Filter):
            raise TypeError("Can only combine filters")
        return CompositeFilter([self, other], "or")
    
    def __xor__(self, other):
        if not isinstance(other, Filter):
            raise TypeError("Can only combine filters")
        return CompositeFilter([self, other], "xor")

class EmptyFilter(Filter):
    def filter(self, *args):
        return True

class CompositeFilter(Filter):
    def __init__(self, filters : list[Filter] = [], action="and"):
        self.filters = filters
        self.action = action
        if action == "xor" and len(filters) != 2:
            raise Exception("XOR filter needs exactly 2 filters")

    def filter(self, *args) -> bool:
        if self.action == "and":
            return all([f.filter(*args) for f in self.filters])
        elif self.action == "or":
            return any([f.filter(*args) for f in self.filters])
        elif self.action == "xor":
            return (self.filters[0].filter(*args) ^ self.filters[1].filter(*args))
        else:
            raise Exception("Unknown action: " + self.action)

class NegationFilter(Filter):
    def __init__(self, filter : Filter):
        self.inner_filter = filter

    def filter(self, *args):
        return not self.inner_filter.filter(*args)
