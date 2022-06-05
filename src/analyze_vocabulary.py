import argparse, sys
from xmlrpc.client import FastUnmarshaller

from .categorizing.time_categorizer import YearCategorizer
from .categorizing.message_categorizer import SenderCategorizer, TypeCategorizer
from .filtering.category_filter import CategoryFilter, EqualsFilter
from .lib.lexical_processing import process_word
from .tools.vocabulary_analyzer import VocabularyAnalyzer
from .vocab.vocabulary import Vocabulary
from .filtering.message_filter import TimeFilter
from .lib.loader import gen_messages, parse_folder
from .lib.conversions import date_to_timestamp, decode_fb

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Analyze your messages')
    parser.add_argument('-p', '--person', help='Name(s) of person(s) you want to know characteristic words of', nargs='+')
    parser.add_argument('-t', '--top-senders', help='Number of top senders to show', default=0, const=10, type=int, nargs='?')
    parser.add_argument('-n', '--number-of-words', help='Number of words to print per person', default=10, type=int)
    parser.add_argument('-v', '--verbose', help='Additional info', action='count', default=0)
    parser.add_argument('-a', '--average-vocab', help='Print average vocabulary at the end', action='store_true')
    parser.add_argument('-y', '--year', help='Characteristic vocab for a given year', type=int)
    parser.add_argument('-i', '--input', help='Your Facebook data folder (should contain the folder "messages" inside it)')

    args = parser.parse_args()

    vocab_analyzer = VocabularyAnalyzer(SenderCategorizer(), args.input, args.verbose)

    vocab_analyzer.generate_vocabulary()
    vocab_analyzer.calculate_average_vocab()

    print("--------------------")
    print("DONE")
    print("--------------------")

    n_senders = args.top_senders
    n_words = args.number_of_words

    if (args.person != None):
        for sender in args.person:
            print(sender, vocab_analyzer.vocabs_by_category[sender].message_count, "messages")
            vocab = vocab_analyzer.get_relative_vocab(EqualsFilter(SenderCategorizer(), sender), 0.01)
            vocab.print(n_words)
            print("Characteristic words:")
            vocab.print(n_words, True)

    vocab_analyzer.print_top(n_senders, n_words)

    if args.average_vocab:
        print("")
        print("Total vocabulary:")
        vocab_analyzer.get_vocab().print(n_words)
    
    if args.year:
        filter = EqualsFilter(TypeCategorizer(), "Generic")
        filter &= EqualsFilter(YearCategorizer(), int(args.year))

        #TODO: Why the heck do I need a different bias here?
        vocab = vocab_analyzer.get_relative_vocab(filter, 30, False)
        # vocab.print(n_words)
        print("Characteristic words:")
        vocab.print(n_words, True)
