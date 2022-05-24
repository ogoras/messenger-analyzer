from lib import decode_fb, print_message

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

    def add_message_to_vocabulary(self, message, words_to_match = []):
        if (self.print_next > 0):
                print_message(message)
                self.print_next -= 1
                if self.print_next == 0:
                    print("----------")

        if "content" in message and message["type"] == "Generic":
            sender = decode_fb(message["sender_name"])
            if sender not in self.all_vocabularies:
                self.all_vocabularies[sender] = {}
            vocabulary = self.all_vocabularies[sender]

            content = decode_fb(message["content"])

            for word in content.split():
                word = word.lower()
                #check if words starts with XDDDD...
                if word.startswith("x" + "d" * 5000) or word in words_to_match:
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