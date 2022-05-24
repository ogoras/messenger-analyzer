import os, sys, argparse

from vocabulary import print_vocab, VocabularyAnalyzer

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Analyze your messages')
    parser.add_argument('-p', '--person', help='Name(s) of person(s) you want to know characteristic words of', nargs='+')
    parser.add_argument('-t', '--top-senders', help='Number of top senders to show', default=0, const=10, type=int, nargs='?')
    parser.add_argument('-n', '--number-of-words', help='Number of words to print per person', default=10, type=int)
    parser.add_argument('-w', '--words-to-match', help='Words to match (separated by commas)', default="")
    parser.add_argument('-v', '--verbose', help='Additional info', action='count', default=0)
    parser.add_argument('-a', '--average-vocab', help='Print average vocabulary at the end', action='store_true')

    args = parser.parse_args()

    vocab_analyzer = VocabularyAnalyzer()

    vocab_analyzer.load_vocab()

    words_to_match = args.words_to_match.split()
    if (args.verbose > 0):
        print("Words to match:", words_to_match)
    #TODO: add words_to_match to or use another class for this

    print("--------------------")
    print("DONE")
    print("--------------------")

    n_senders = args.top_senders
    n_words = args.number_of_words

    if (args.person != None):
        for sender in args.person:
            print(sender, vocab_analyzer.messages_count[sender])
            print_vocab(vocab_analyzer.get_vocab(sender), n_words)
            print("Characteristic words:")
            print_vocab(vocab_analyzer.characteristic_vocab(sender), n_words, vocab_analyzer.get_vocab(sender), vocab_analyzer.get_vocab())

    vocab_analyzer.print_top(n_senders, n_words)

    if args.average_vocab:
        print("")
        print("Total vocabulary:")
        print_vocab(vocab_analyzer.get_vocab(), n_words)