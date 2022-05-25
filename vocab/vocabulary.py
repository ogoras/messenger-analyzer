#TODO: move all functions into the class
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

class Vocabulary:
    def __init__(self, from_json=None):
        self.dict = {}
        self.normalized = None  #dict
        self.sorted = None      #list

        self.message_count = 0
        self.word_count = 0
        self.distinct_word_count = 0

        if from_json != None:
            self.dict = from_json["dict"]
            self.message_count = from_json["message_count"]
            self.word_count = from_json["word_count"]
            self.distinct_word_count = from_json["distinct_word_count"]
            self.normalized = from_json["normalized"]
            self.sorted = from_json["sorted"]
    
    def increment(self, word, increment=1):
        self.sorted = None
        self.normalized = None

        self.dict[word] = self.dict.get(word, 0) + increment
        self.word_count += increment

        if word not in self.dict:
            self.distinct_word_count += 1
    
    def increment_message(self):
        self.message_count += 1

    def normalize(self, bias=0):
        if self.normalized == None:
            self.normalized = normalize_vocab(self.dict, bias)
        return self.normalized

    def sort(self):
        if self.sorted == None:
            self.sorted = sorted(self.dict, key=self.dict.get, reverse=True)
        return self.sorted

