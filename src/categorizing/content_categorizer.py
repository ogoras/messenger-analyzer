from abc import abstractmethod
from .message_categorizer import MessageCategorizer
from ..lib.lexical_processing import match_words, process_word

class ContentCategorizer(MessageCategorizer):
    def categorize_message(self, message):
        if "content" in message:
            return self.categorize_content(message["content"])
        else:
            return None

    @abstractmethod
    def categorize_content(self, content):
        pass

class WordCountCategorizer(ContentCategorizer): #TODO: use WFilter instead
    def __init__(self, patterns=None, match="whole"):
        self.patterns = patterns
        self.match = match

    def categorize_content(self, content):
        if not self.patterns:
            return len(content.split())
        else:
            return len([process_word(word) for word in content.split() if any([match_words(pattern, process_word(word), self.match) for pattern in self.patterns])])