from lib.lexical_processing import process_word, match_words
from lib.conversions import print_message, decode_fb

#TODO: change this class into sth more like "MessageFinder", and just use a filter inside search_message :)
class WordFinder:
    def __init__(self, words_to_match = [], verbosity = 0, match = "whole"):
        self.message_cache = None
        self.print_next = 0
        self.words_to_match = words_to_match
        self.verbosity = verbosity
        self.message_count = 0
        self.count = 0
        self.counts_by_sender = {}
        self.messages_by_sender = {}
        self.match = match

    def search_message(self, message):
        if (self.print_next > 0):
            print_message(message)
            self.print_next -= 1
            if self.print_next == 0:
                print("----------")

        sender = decode_fb(message["sender_name"])
        
        if "content" in message:
            content = decode_fb(message["content"])

            ignore_this_message = False

            for word in content.split():
                word = process_word(word)

                if any([match_words(pattern, word, self.match) for pattern in self.words_to_match]):
                    self.count += 1
                    self.counts_by_sender[sender] = self.counts_by_sender.get(sender, 0) + 1

                    if not ignore_this_message:
                        self.message_count += 1
                        self.messages_by_sender[sender] = self.messages_by_sender.get(sender, 0) + 1
                        if self.message_cache != None and self.print_next == 0:
                            print_message(self.message_cache)
                        if self.verbosity > 1 and self.print_next == 0:
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