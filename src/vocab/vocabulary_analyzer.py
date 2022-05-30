from ..categorizing.categorizer import Categorizer
from ..categorizing.message_categorizer import SenderCategorizer
from ..lib import loader
from .vocabulary import Vocabulary
from ..lib.conversions import decode_fb
from ..lib.lexical_processing import process_word

class VocabularyAnalyzer:
    def __init__(self, categorizer : Categorizer = SenderCategorizer()):
        #TODO: add master folder as a parameter
        #TODO: relative vocabs as a function, not fields
        self.vocabs_by_category : dict[any, Vocabulary] = {}
        self.average_vocab = Vocabulary()
        self.total_vocab = Vocabulary()
        self.categorizer = categorizer

        self.sorted = False

    def add_message_to_vocabulary(self, message):
        self.sorted = False

        if "content" in message:
            #TODO: not just message categorizing
            category = self.categorizer.categorize("", "", None, message)

            if category not in self.vocabs_by_category:
                self.vocabs_by_category[category] = Vocabulary()
                
            vocab_by_sender = self.vocabs_by_category[category]

            content = decode_fb(message["content"])

            vocab_by_sender.increment_message()
            self.total_vocab.increment_message()

            for word in content.split():
                word = process_word(word)
                vocab_by_sender.increment(word)
                self.total_vocab.increment(word)

    def calculate_average_vocab(self):
        self.sorted = False
        self.average_vocab = Vocabulary()

        for category in self.vocabs_by_category:
            magnitude_order = len(str(self.vocabs_by_category[category].distinct_word_count))
            for word in self.vocabs_by_category[category].dict:
                self.average_vocab.increment(word, self.vocabs_by_category[category].dict[word]/self.vocabs_by_category[category].word_count*magnitude_order)
        
        self.average_vocab.normalize(0.01)

    def get_vocab(self, category = None):
        if category == None:
            return self.total_vocab
        else:
            return self.vocabs_by_category[category]

    def print_characteristic_vocab(self, category, n_words=10):
        self.vocabs_by_category[category].relate(self.average_vocab)
        self.vocabs_by_category[category].print(n_words, True, self.get_vocab().dict)

    def save_vocab(self):
        if (self.sorted == False):
            self.sort()
        loader.save(self, "vocab.json")
    
    def load_vocab(self):
        self.sorted = True
        data = loader.load("vocab.json")
        self.vocabs_by_category = {}
        for category in data["vocabs_by_category"]:
            self.vocabs_by_category[category] = Vocabulary(data["vocabs_by_category"][category])
        self.total_vocab = Vocabulary(data["total_vocab"])
        self.average_vocab = Vocabulary(data["average_vocab"])

    def sort(self):
        if self.sorted == True:
            return
        self.sorted = True
        for category in self.vocabs_by_category:
            self.vocabs_by_category[category].sort()
        self.average_vocab.sort()
        self.total_vocab.sort()
    
    def print_top(self, n_senders=10, n_words=10):
        messages_count_sorted = sorted(self.vocabs_by_category, key=lambda x: self.vocabs_by_category[x].message_count, reverse=True)

        for sender in messages_count_sorted[:n_senders]:
            print(sender, self.vocabs_by_category[sender].message_count)
            self.print_characteristic_vocab(sender, n_words)