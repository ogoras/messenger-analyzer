from filtering.filter import CompositeFilter
from filtering.message_filter import MessageFilter
from abc import abstractmethod
from filtering.wfilter import MatchWFilter
from lib.conversions import decode_fb

from lib.lexical_processing import match_words, process_word

class ContentFilter(MessageFilter):
    def filter_message(self, message):
        return "content" in message and self.filter_content(decode_fb(message["content"]))

    @abstractmethod
    def filter_content(self, content):
        pass

class WordFilter(ContentFilter):
    def __init__(self, wfilter, action="or"):
        self.wfilter = wfilter
        self.action = action

        #TODO: override __and__, __or__, __xor__ methods ?? -think about it!!

    def filter_content(self, content):
        if self.action == "or":
            return any([self.filter_word(word) for word in content.split()])
        elif self.action == "and":
            return all([self.filter_word(word) for word in content.split()])
        #TODO: write the rest
    
    def filter_word(self, word):
        return self.wfilter.filter(word)

def words_filter(words, match="whole", action="or"):
    return CompositeFilter([WordFilter(MatchWFilter(word, match), action) for word in words], "or")