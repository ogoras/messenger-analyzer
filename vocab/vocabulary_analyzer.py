import lib.loader as loader

from vocab.vocabulary import Vocabulary, relative_vocab, print_vocab
from lib.conversions import decode_fb
from lib.lexical_processing import process_word

class VocabularyAnalyzer:
    def __init__(self):    
        self.vocabs_by_sender = {}
        self.average_vocab = Vocabulary()
        self.total_vocab = Vocabulary()

        self.sorted = False

    def add_message_to_vocabulary(self, message):
        self.sorted = False

        if "content" in message and message["type"] == "Generic":
            sender = decode_fb(message["sender_name"])

            if sender not in self.vocabs_by_sender:
                self.vocabs_by_sender[sender] = Vocabulary()
                
            vocab_by_sender = self.vocabs_by_sender[sender]

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

        for sender in self.vocabs_by_sender:
            magnitude_order = len(str(self.vocabs_by_sender[sender].distinct_word_count))
            for word in self.vocabs_by_sender[sender].dict:
                self.average_vocab.increment(word, self.vocabs_by_sender[sender].dict[word]/self.vocabs_by_sender[sender].word_count*magnitude_order)
        
        self.average_vocab.normalize(0.001)

    def get_vocab(self, sender = None):
        if sender == None:
            return self.total_vocab.dict
        else:
            return self.vocabs_by_sender[sender].dict

    def characteristic_vocab(self, sender):
        return relative_vocab(self.vocabs_by_sender[sender].normalize(), self.average_vocab.normalized)

    def save_vocab(self):
        if (self.sorted == False):
            self.sort()
        loader.save(self, "vocab.json")
    
    def load_vocab(self):
        self.sorted = True
        data = loader.load("vocab.json")
        self.vocabs_by_sender = {}
        for sender in data["vocabs_by_sender"]:
            self.vocabs_by_sender[sender] = Vocabulary(data["vocabs_by_sender"][sender])
        self.total_vocab = Vocabulary(data["total_vocab"])
        self.average_vocab = Vocabulary(data["average_vocab"])

    def sort(self):
        if self.sorted == True:
            return
        self.sorted = True
        for sender in self.vocabs_by_sender:
            self.vocabs_by_sender[sender].sort()
        self.average_vocab.sort()
        self.total_vocab.sort()
    
    def print_top(self, n_senders=10, n_words=10):
        messages_count_sorted = sorted(self.vocabs_by_sender, key=lambda x: self.vocabs_by_sender[x].message_count, reverse=True)

        for sender in messages_count_sorted[:n_senders]:
            print(sender, self.vocabs_by_sender[sender].message_count)
            print_vocab(self.characteristic_vocab(sender), n_words, self.get_vocab(sender), self.get_vocab())
