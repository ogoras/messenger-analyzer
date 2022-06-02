from src.filtering.filter import EmptyFilter
from ..categorizing.categorizer import Categorizer
from ..categorizing.message_categorizer import SenderCategorizer
from ..lib import loader
from ..vocab.vocabulary import Vocabulary
from ..lib.conversions import decode_fb
from ..lib.lexical_processing import process_word

class VocabularyAnalyzer:
    def __init__(self, categorizer : Categorizer = SenderCategorizer(), path = None, verbose = 0):
        self.vocabs_by_category : dict[any, Vocabulary] = {}
        self.average_vocab = Vocabulary()
        self.total_vocab = Vocabulary()
        self.categorizer = categorizer

        self.sorted = False
        self.path = loader.parse_folder(path, "<script name>")
        self.verbose = verbose

    def generate_vocabulary(self):
        for (subfolder, conversation_folder, thread, message) in loader.gen_messages(self.path, EmptyFilter(), verbose = self.verbose > 1):
            self.add_message_to_vocabulary(subfolder, conversation_folder, thread, message)

    def add_message_to_vocabulary(self, subfolder, conversation_folder, thread, message):
        self.sorted = False

        if "content" in message:
            category = self.categorizer.categorize(subfolder, conversation_folder, thread, message)

            if category not in self.vocabs_by_category:
                self.vocabs_by_category[category] = Vocabulary()
                
            vocab_by_sender = self.vocabs_by_category[category]

            content = decode_fb(message["content"])

            vocab_by_sender.add_content(content)
            self.total_vocab.add_content(content)

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

    def get_relative_vocab(self, filter, scaled=True):
        relative_vocab = Vocabulary()
        for (subfolder, conversation_folder, thread, message) in loader.gen_messages(self.path, filter):
            if "content" in message:
                content = decode_fb(message["content"])
                relative_vocab.add_content(content)
        if scaled:
            relative_vocab.relate(self.average_vocab)
        else:
            relative_vocab.relate(self.total_vocab)
        return relative_vocab

    def print_characteristic_vocab(self, category, n_words=10, scaled=True):
        if scaled:
            self.vocabs_by_category[category].relate(self.average_vocab)
        else:
            self.vocabs_by_category[category].relate(self.total_vocab)
        self.vocabs_by_category[category].print(n_words, True, self.get_vocab().dict)

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

    # def save_vocab(self):
    #     if (self.sorted == False):
    #         self.sort()
    #     loader.save(self, "vocab.json")
    
    # def load_vocab(self):
    #     self.sorted = True
    #     data = loader.load("vocab.json")
    #     self.vocabs_by_category = {}
    #     for category in data["vocabs_by_category"]:
    #         self.vocabs_by_category[category] = Vocabulary(data["vocabs_by_category"][category])
    #     self.total_vocab = Vocabulary(data["total_vocab"])
    #     self.average_vocab = Vocabulary(data["average_vocab"])