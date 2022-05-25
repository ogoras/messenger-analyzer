import argparse, sys
from lib.lexical_processing import process_word

from vocab.vocabulary_analyzer import VocabularyAnalyzer
from vocab.vocabulary import Vocabulary
from lib.filter import TimeFilter, TypeFilter
from lib.loader import gen_messages, parse_folder
from lib.conversions import date_to_timestamp, decode_fb

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

    vocab_analyzer = VocabularyAnalyzer()

    vocab_analyzer.load_vocab()

    print("--------------------")
    print("DONE")
    print("--------------------")

    n_senders = args.top_senders
    n_words = args.number_of_words

    if (args.person != None):
        for sender in args.person:
            print(sender, vocab_analyzer.vocabs_by_sender[sender].message_count, "messages")
            vocab_analyzer.get_vocab(sender).print(n_words)
            print("Characteristic words:")
            vocab_analyzer.print_characteristic_vocab(sender, n_words)

    vocab_analyzer.print_top(n_senders, n_words)

    if args.average_vocab:
        print("")
        print("Total vocabulary:")
        vocab_analyzer.get_vocab().print(n_words)
    
    if args.year:
        master_folder = parse_folder(args.input, sys.argv[0])
        filter = TypeFilter("Generic")
        filter = filter.join(TimeFilter(date_to_timestamp(args.year), date_to_timestamp(args.year + 1)))
        year_vocab = Vocabulary()

        for message in gen_messages(master_folder, filter):
            if "content" in message:
                year_vocab.increment_message()
                content = decode_fb(message["content"])

                for word in content.split():
                    word = process_word(word)
                    year_vocab.increment(word)
        
        year_vocab.relate(vocab_analyzer.get_vocab())
        year_vocab.print(n_words, True, vocab_analyzer.get_vocab().dict)
