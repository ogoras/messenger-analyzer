from src.categorizing.categorizer import Categorizer
from src.categorizing.message_categorizer import SenderCategorizer
from ..categorizing.counter import Counter
from ..lib.conversions import print_message, decode_fb

class MessageFinder:
    def __init__(self, counter, verbosity = 0, categorizer = SenderCategorizer()):
        self.message_cache = None
        self.print_next = 0
        self.counter = counter
        self.counting = isinstance(counter, Counter)
        self.verbosity = verbosity
        self.message_count = 0
        self.count = 0
        self.counts_by_category = {}
        self.messages_by_category = {}
        self.categorizer = categorizer

    def search_message(self, subfolder, conversation_folder, thread, message):
        if (self.print_next > 0):
            print_message(message)
            self.print_next -= 1
            if self.print_next == 0:
                print("----------")

        category = self.categorizer.categorize(subfolder, conversation_folder, thread, message)
        
        filter_this = None

        if self.counting:
            count = self.counter.categorize(subfolder, conversation_folder, thread, message) or 0
            filter_this = count > 0
            self.count += count if filter_this else 0
            self.counts_by_category[category] = self.counts_by_category.get(category, 0) + (count if filter_this else 0)
        else:
            filter_this = self.counter.filter(subfolder, conversation_folder, thread, message)

        if filter_this:
            self.message_count += 1
            self.messages_by_category[category] = self.messages_by_category.get(category, 0) + 1
            if self.message_cache != None and self.print_next == 0:
                print_message(self.message_cache)
            if self.verbosity > 1 and self.print_next == 0:
                print_message(message)
            self.print_next = self.verbosity - 2 if self.verbosity > 1 else 0

        if self.verbosity > 3:
            self.message_cache = message
    
    def print_results(self):
        print_string = "Found "
        if self.counting:
            print_string += str(self.count) + " occurences in "
        print_string += str(self.message_count) + " messages"
        print(print_string)

        if self.verbosity > 0:
            print("")
            print("Number of occurences by category:")
            for category in sorted(self.messages_by_category):
                print_string = str(category) + ": "
                if self.counting:
                    print_string += str(self.counts_by_category[category]) + " occurences in "
                print_string += str(self.messages_by_category[category]) + " messages"
                print(print_string)
            print("")