import argparse, sys
from lib.conversions import date_to_timestamp

from lib.loader import gen_messages, parse_folder
from vocab.word_finder import WordFinder
from filtering.message_filter import senders_filter, TimeFilter
from filtering.category_filter import EqualsFilter
from categorizing.message_categorizer import TypeCategorizer

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
        if args.month:
            if args.month == 12:
                filter &= TimeFilter(date_to_timestamp(args.year, 12), date_to_timestamp(args.year + 1, 1))
            else:
                filter &= TimeFilter(date_to_timestamp(args.year, args.month), date_to_timestamp(args.year, args.month + 1))
        else:
            filter &= TimeFilter(date_to_timestamp(args.year), date_to_timestamp(args.year + 1))
    if args.filter_senders:
        filter_to_add = senders_filter(args.filter_senders)

        if args.filter_senders_inverse:
            filter_to_add = ~filter_to_add

        filter &= filter_to_add

    word_finder = WordFinder(args.words_to_match.split(), args.verbose, args.match)
    # move filter_senders to gen_messages
    for message in gen_messages(master_folder, filter):
        word_finder.search_message(message)

    word_finder.print_results()
