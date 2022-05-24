from lib import decode_fb, print_message
import loader

def print_vocab(vocabulary, n=100, overall_vocabulary=None, master_vocabulary=None):
    print("Vocabulary size: " + str(len(vocabulary)))
    i = 0
    for word in sorted(vocabulary, key=vocabulary.get, reverse=True)[:n]:
        i += 1
        print_string = str(i) + ". " + word + " " + str(vocabulary[word])
        if overall_vocabulary != None:
            print_string += " used " + str(overall_vocabulary[word]) + " times"
            if master_vocabulary != None: 
                print_string += " out of " + str(master_vocabulary[word])
        print(print_string)
    print("")

def relative_vocab(vocabulary, master_vocabulary):
    relative_vocabulary = {}
    for word in vocabulary:
        relative_vocabulary[word] = vocabulary[word]/ master_vocabulary[word]
    return relative_vocabulary

def normalize_vocab(vocabulary, bias=0):
    sum = 0.0
    for word in vocabulary:
        sum += vocabulary[word] + bias

    normalized = {}
    for word in vocabulary:
        normalized[word] = (vocabulary[word] + bias) * 100/sum
    return normalized

class VocabularyAnalyzer:
    def __init__(self):    
        self.all_vocabularies = {}
        self.total_words = {}
        self.average_vocabulary = {}
        self.vocabulary_sizes = {}
        self.total_vocabulary = {}
        self.average_vocabulary_normalized = None
        self.message_cache = None
        self.print_next = 0
        self.messages_count = {}
        self.sorted = False

        self.all_vocabularies_sorted = {}
        self.total_words_sorted = []
        self.average_vocabulary_sorted = []
        self.vocabulary_sizes_sorted = []
        self.total_vocabulary_sorted = []
        self.average_vocabulary_normalized_sorted = []
        self.messages_count_sorted = []

    def add_message_to_vocabulary(self, message, words_to_match = []):
        self.sorted = False
        if (self.print_next > 0):
                print_message(message)
                self.print_next -= 1
                if self.print_next == 0:
                    print("----------")

        if "content" in message and message["type"] == "Generic":
            sender = decode_fb(message["sender_name"])

            if sender not in self.all_vocabularies:
                self.messages_count[sender] = 0
                self.all_vocabularies[sender] = {}
            self.messages_count[sender] += 1
            vocabulary = self.all_vocabularies[sender]

            content = decode_fb(message["content"])

            ignore_this_message = False
            for word in content.split():
                #strip punctuation
                word = word.strip('.,!?;:*()[]{}<>…"\'/\\”“')
                word = word.lower()
                #check if words starts with XDDDD...
                if word.startswith("x" + "d" * 5000) or word in words_to_match and not ignore_this_message:
                    ignore_this_message = True
                    if self.message_cache != None:
                        print_message(self.message_cache)
                    print_message(message)
                    self.print_next = 7
                if word in vocabulary:
                    vocabulary[word] += 1
                else:
                    vocabulary[word] = 1
                if sender in self.total_words:
                    self.total_words[sender] += 1
                else:
                    self.total_words[sender] = 1
            
            self.message_cache = message

    def calculate_average_vocab(self):
        self.sorted = False
        self.average_vocabulary = {}
        self.total_vocabulary = {}

        for sender in self.all_vocabularies:
            self.vocabulary_sizes[sender] = len(self.all_vocabularies[sender])

        for sender in self.all_vocabularies:
            magnitude_order = len(str(self.vocabulary_sizes[sender]))
            for word in self.all_vocabularies[sender]:
                if word in self.average_vocabulary:
                    self.total_vocabulary[word] += self.all_vocabularies[sender][word]
                    self.average_vocabulary[word] += self.all_vocabularies[sender][word]/self.total_words[sender]*magnitude_order
                else:
                    self.total_vocabulary[word] = self.all_vocabularies[sender][word]
                    self.average_vocabulary[word] = self.all_vocabularies[sender][word]/self.total_words[sender]*magnitude_order
        
        self.average_vocabulary_normalized = normalize_vocab(self.average_vocabulary, 0.01)

    def get_vocab(self, sender = None):
        if sender == None:
            return self.total_vocabulary
        else:
            return self.all_vocabularies[sender]

    def characteristic_vocab(self, sender):
        return relative_vocab(normalize_vocab(self.all_vocabularies[sender]), self.average_vocabulary_normalized)

    def save_vocab(self):
        if (self.sorted == False):
            self.sort()
        loader.save_vocab ({
            "all_vocabularies": self.all_vocabularies,
            "total_words": self.total_words,
            "average_vocabulary": self.average_vocabulary,
            "vocabulary_sizes": self.vocabulary_sizes,
            "total_vocabulary": self.total_vocabulary,
            "average_vocabulary_normalized": self.average_vocabulary_normalized,
            "messages_count": self.messages_count,
            "all_vocabularies_sorted": self.all_vocabularies_sorted,
            "total_words_sorted": self.total_words_sorted,
            "average_vocabulary_sorted": self.average_vocabulary_sorted,
            "vocabulary_sizes_sorted": self.vocabulary_sizes_sorted,
            "total_vocabulary_sorted": self.total_vocabulary_sorted,
            "average_vocabulary_normalized_sorted": self.average_vocabulary_normalized_sorted,
            "messages_count_sorted": self.messages_count_sorted
        })
    
    def load_vocab(self):
        self.sorted = True
        data = loader.load_vocab()
        self.all_vocabularies = data["all_vocabularies"]
        self.total_words = data["total_words"]
        self.average_vocabulary = data["average_vocabulary"]
        self.vocabulary_sizes = data["vocabulary_sizes"]
        self.total_vocabulary = data["total_vocabulary"]
        self.average_vocabulary_normalized = data["average_vocabulary_normalized"]
        self.messages_count = data["messages_count"]
        self.all_vocabularies_sorted = data["all_vocabularies_sorted"]
        self.total_words_sorted = data["total_words_sorted"]
        self.average_vocabulary_sorted = data["average_vocabulary_sorted"]
        self.vocabulary_sizes_sorted = data["vocabulary_sizes_sorted"]
        self.total_vocabulary_sorted = data["total_vocabulary_sorted"]
        self.average_vocabulary_normalized_sorted = data["average_vocabulary_normalized_sorted"]
        self.messages_count_sorted = data["messages_count_sorted"]

    def sort(self):
        self.sorted = True
        for sender in self.all_vocabularies:
            self.all_vocabularies_sorted[sender] = sorted(self.all_vocabularies[sender], key=self.all_vocabularies[sender].get, reverse=True)
        self.average_vocabulary_sorted = sorted(self.average_vocabulary, key=self.average_vocabulary.get, reverse=True)
        self.vocabulary_sizes_sorted = sorted(self.vocabulary_sizes, key=self.vocabulary_sizes.get, reverse=True)
        self.total_vocabulary_sorted = sorted(self.total_vocabulary, key=self.total_vocabulary.get, reverse=True)
        self.average_vocabulary_normalized_sorted = sorted(self.average_vocabulary_normalized, key=self.average_vocabulary_normalized.get, reverse=True)
        self.messages_count_sorted = sorted(self.messages_count, key=self.messages_count.get, reverse=True)
        self.total_words_sorted = sorted(self.total_words, key=self.total_words.get, reverse=True)
    
    def print_top(self, n_senders=10, n_words=10):
        for sender in self.messages_count_sorted[:n_senders]:
            print(sender, self.messages_count[sender])
            print_vocab(self.characteristic_vocab(sender), n_words, self.get_vocab(sender), self.get_vocab())
