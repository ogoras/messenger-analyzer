from filtering.filter import Filter
from abc import abstractmethod

from lib.lexical_processing import match_words, process_word

class WFilter(Filter):
    def filter(self, word):
        pass

class MatchWFilter(WFilter):
    def __init__(self, pattern, match="whole"):
        self.pattern = pattern
        self.match = match

    def filter(self, word):
        return match_words(self.pattern, process_word(word), self.match)

class CapitalizationWFilter(WFilter):
    def filter(self, word):
        return word.isupper()