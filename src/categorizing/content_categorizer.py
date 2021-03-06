from abc import abstractmethod

from src.lib.conversions import decode_fb

from ..filtering.wfilter import WFilter
from .message_categorizer import MessageCategorizer
from ..lib.lexical_processing import match_words, process_word
from .counter import Counter

class ContentCategorizer(MessageCategorizer):
    def categorize_message(self, message):
        return "content" in message and self.categorize_content(decode_fb(message["content"]))

    @abstractmethod
    def categorize_content(self, content : str):
        pass

class WordCounter(ContentCategorizer, Counter):
    def __init__(self, wfilter : WFilter):
        self.wfilter = wfilter

    def categorize_content(self, content) -> int:
        return len([process_word(word) for word in content.split() if self.wfilter.filter(process_word(word))])