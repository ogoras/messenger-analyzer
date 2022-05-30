from abc import abstractmethod

from ..filtering.wfilter import WFilter
from .message_categorizer import MessageCategorizer
from ..lib.lexical_processing import match_words, process_word
from .counter import Counter

class ContentCategorizer(MessageCategorizer):
    def categorize_message(self, message):
        if "content" in message:
            return self.categorize_content(message["content"])
        else:
            return None

    @abstractmethod
    def categorize_content(self, content : str):
        pass

class WordCounter(ContentCategorizer, Counter):
    def __init__(self, wfilter : WFilter):
        self.wfilter = wfilter

    def categorize_content(self, content) -> int:
        return len([process_word(word) for word in content.split() if self.wfilter.filter(process_word(word))])