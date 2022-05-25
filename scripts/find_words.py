import argparse, os, sys

from lib.loader import read_folder
from lib.conversions import parse_folder
from vocab.word_finder import WordFinder

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate a vocabulary data file')
    parser.add_argument('-i', '--input', help='Your Facebook data folder (should contain the folder "messages" inside it)')
    parser.add_argument('-v', '--verbose', help='Additional info', action='count', default=0)
    parser.add_argument('-w', '--words-to-match', help='Words to match', required=True)
    parser.add_argument('-f', '--filter-senders', help='Senders to filter', nargs='+')
    parser.add_argument('-F', '--filter-senders-inverse', help='Inverse filter', action='store_true', default=False)

    args = parser.parse_args()

    master_folder = parse_folder(args.input, sys.argv[0])

    filter_senders = []
    if args.filter_senders:
        filter_senders = args.filter_senders

    word_finder = WordFinder(args.words_to_match.split(), args.verbose, filter_senders, args.filter_senders_inverse)

    for conversation_folder in os.listdir(master_folder):
        conversation_folder = os.path.join(master_folder, conversation_folder)
        messages = read_folder(conversation_folder)
        # if (args.verbose > 1):
        #     print_fb(messages[0]["title"])
        for message_file in messages:
            for message in message_file["messages"]:
                word_finder.search_message(message)

    word_finder.print_results()
