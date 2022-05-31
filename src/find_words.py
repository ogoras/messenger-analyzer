import argparse, sys

from .filtering.filter import CompositeFilter
from .categorizing.content_categorizer import WordCounter
from .categorizing.time_categorizer import MonthCategorizer, YearCategorizer
from .filtering.content_filter import WordFilter, words_filter
from .filtering.wfilter import CapitalizationWFilter, MatchWFilter
from .lib.loader import gen_messages, parse_folder
from .tools.message_finder import MessageFinder
from .filtering.message_filter import senders_filter
from .filtering.category_filter import EqualsFilter
from .categorizing.message_categorizer import TypeCategorizer

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate a vocabulary data file')
    parser.add_argument('-i', '--input', help='Your Facebook data folder (should contain the folder "messages" inside it)')
    parser.add_argument('-v', '--verbose', help='Additional info', action='count', default=0)
    parser.add_argument('-w', '--words-to-match', help='Words to match', required=True)
    parser.add_argument('-f', '--filter-senders', help='Senders to filter', nargs='+')
    parser.add_argument('-F', '--filter-senders-inverse', help='Inverse filter', action='store_true', default=False)
    parser.add_argument('-y', '--year', help='Year to filter', type=int)
    parser.add_argument('-m', '--month', help='Month to filter', type=int)
    parser.add_argument('--match', help='Match type', choices=['whole', 'left', 'right', 'contains'], default='whole')

    args = parser.parse_args()

    master_folder = parse_folder(args.input, sys.argv[0])

    filter = EqualsFilter(TypeCategorizer(), "Generic")
    if args.year:
        filter &= EqualsFilter(YearCategorizer(), args.year)
    if args.month:
        filter &= EqualsFilter(MonthCategorizer(), args.month)
    if args.filter_senders:
        filter_to_add = senders_filter(args.filter_senders)

        if args.filter_senders_inverse:
            filter_to_add = ~filter_to_add

        filter &= filter_to_add
    
    word_finder = MessageFinder(WordCounter(CompositeFilter([MatchWFilter(word, "whole") for word in args.words_to_match.split()], "or")), args.verbose) #, YearCategorizer())

    # lightweight version
    #word_finder = WordFinder(words_filter(args.words_to_match.split(), args.match), args.verbose)

    # Example: Find messages where all words are capitalized, but don't include XDD...
    #word_finder = MessageFinder(WordFilter(CapitalizationWFilter() & ~MatchWFilter("xd", "left"), "and"), args.verbose)

    for (subfolder, conversation_folder, thread, message) in gen_messages(master_folder, filter):
        word_finder.search_message(subfolder, conversation_folder, thread, message)

    word_finder.print_results()
