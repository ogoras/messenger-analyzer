from lib.lexical_processing import process_word
from lib.conversions import print_message, decode_fb

class WordFinder:
    def __init__(self, words_to_match = [], verbosity = 0, filter_senders = [], filter_senders_inverse = False):
        self.message_cache = None
        self.print_next = 0
        self.words_to_match = words_to_match
        self.verbosity = verbosity
        self.message_count = 0
        self.count = 0
        self.counts_by_sender = {}
        self.messages_by_sender = {}
        self.filter_senders = filter_senders
        self.filter_senders_inverse = filter_senders_inverse

    def search_message(self, message):
        if (self.print_next > 0):
            print_message(message)
            self.print_next -= 1
            if self.print_next == 0:
                print("----------")

        sender = decode_fb(message["sender_name"])

        if "content" in message and message["type"] == "Generic" and ((sender not in self.filter_senders) ^ (self.filter_senders_inverse)):
            content = decode_fb(message["content"])

            ignore_this_message = False

            for word in content.split():
                word = process_word(word)

                if word in self.words_to_match:
                    self.count += 1
                    self.counts_by_sender[sender] = self.counts_by_sender.get(sender, 0) + 1

                    if not ignore_this_message:
                        self.message_count += 1
                        self.messages_by_sender[sender] = self.messages_by_sender.get(sender, 0) + 1
                        if self.message_cache != None:
                            print_message(self.message_cache)
                        if self.verbosity > 1:
                            print_message(message)
                        self.print_next = self.verbosity - 2 if self.verbosity > 1 else 0
                        ignore_this_message = True

        if self.verbosity > 3:
            self.message_cache = message
    
    def print_results(self):
        print("Found " + str(self.count) + " words in " + str(self.message_count) + " messages")
        if self.verbosity > 0:
            print("")
            print("Number of times word(s) were used by sender:")
            for sender in self.counts_by_sender:
                print(sender + ": " + str(self.counts_by_sender[sender]) + " words in " + str(self.messages_by_sender[sender]) + " messages")
            print("")