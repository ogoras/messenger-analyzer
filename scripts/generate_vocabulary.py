import argparse, os, sys

from vocab.vocabulary_analyzer import VocabularyAnalyzer
from lib.loader import gen_messages, parse_folder
from categorizing.message_categorizer import TypeCategorizer
from filtering.category_filter import EqualsFilter

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate a vocabulary data file')
    parser.add_argument('-i', '--input', help='Your Facebook data folder (should contain the folder "messages" inside it)')
    parser.add_argument('-v', '--verbose', help='Additional info', action='count', default=0)

    args = parser.parse_args()

    master_folder = parse_folder(args.input, sys.argv[0])

    vocab_analyzer = VocabularyAnalyzer()

    filter = EqualsFilter(TypeCategorizer(), "Generic")

    for message in gen_messages(master_folder, filter, verbose = args.verbose > 1):
        vocab_analyzer.add_message_to_vocabulary(message)

    vocab_analyzer.calculate_average_vocab()
    vocab_analyzer.save_vocab()
