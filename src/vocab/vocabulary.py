from __future__ import annotations

class Vocabulary:
    def __init__(self, from_json=None):
        self.dict : dict[str, int] = {}
        self.normalized : dict[str, float] = None
        self.sorted : list[str] = None
        self.relative : dict[str, float] = {}
        self.relative_sorted : list[str] = None

        self.message_count : int = 0
        self.word_count : int = 0
        self.distinct_word_count : int = 0
        self.normalization_bias : float = 0
        self.print_first : bool = True

        if from_json != None:
            self.dict = from_json["dict"]
            self.message_count = from_json["message_count"]
            self.word_count = from_json["word_count"]
            self.distinct_word_count = from_json["distinct_word_count"]
            self.normalized = from_json["normalized"]
            self.sorted = from_json["sorted"]
            self.relative = from_json["relative"]
            self.relative_sorted = from_json["relative_sorted"]
            self.normalization_bias = from_json["normalization_bias"]
    
    def increment(self, word, increment=1):
        #TODO: unit tests!
        self.sorted = None
        self.normalized = None

        if word not in self.dict:
            self.distinct_word_count += 1

        self.dict[word] = self.dict.get(word, 0) + increment
        self.word_count += increment
        
    
    def increment_message(self):
        self.message_count += 1

    def normalize(self, bias=0):
        if self.normalized == None or bias != self.normalization_bias:
            self.normalization_bias = bias

            sum = 0.0
            for word in self.dict:
                sum += self.dict[word] + bias
            #TODO: try sum = self.word_count + bias*self.distinct_word_count

            self.normalized = {}
            for word in self.dict:
                self.normalized[word] = (self.dict[word] + bias) * 100/sum

        return self.normalized

    def sort(self):
        if self.sorted == None:
            self.sorted = sorted(self.dict, key=self.dict.get, reverse=True)
        if self.relative_sorted == None:
            self.relative_sorted = sorted(self.relative, key=self.relative.get, reverse=True)
        return self.sorted

    def print(self, n=100, relative=False, master_vocabulary=None, percentage=True):
        self.sort()
        self.normalize(self.normalization_bias)

        if relative:
            sorted = self.relative_sorted
        else:
            sorted = self.sorted

        print("Vocabulary size: " + str(self.distinct_word_count) + " distinct words, " + str(self.word_count) + " words total")
        i = 0
        for word in sorted[:n]:
            i += 1
            print_string = str(i) + ". " + word + " "

            if relative:
                print_string += str(self.relative[word]) + " "

            print_string += "| used " + str(self.dict[word]) + " times"

            if master_vocabulary != None: 
                print_string += " out of " + str(master_vocabulary[word]) + " found overall"
            
            if percentage:
                #print 2 significant digits, not 2 digits after the comma
                print_string += " (" + str(round(self.normalized[word]*10, 2)) + "‰ of vocab) "
            
            print(print_string)
        print("")

    def relate(self, master_vocabulary : Vocabulary):
        self.relative_sorted = None
        self.relative = {}
        #TODO: remove hardcoded bias
        master_vocabulary.normalize(master_vocabulary.normalization_bias)
        
        self.normalize(self.normalization_bias)
        for word in self.normalized:
            self.relative[word] = self.normalized[word] / master_vocabulary.normalized[word]

        return self.relative
