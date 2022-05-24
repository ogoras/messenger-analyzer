from doctest import master
import os, sys, argparse

from loader import read_folder, load_dirs, save_dir
from vocabulary import print_vocab, VocabularyAnalyzer
from lib import decode_fb, print_fb

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Analyze your messages')
    parser.add_argument('-i', '--input', help='Your Facebook data folder (should contain the folder "messages" inside it)')
    parser.add_argument('-p', '--person', help='Name(s) of person(s) you want to know characteristic words of', nargs='+')
    parser.add_argument('-t', '--top-senders', help='Number of top senders to show', default=0, type=int)
    parser.add_argument('-n', '--number-of-words', help='Number of words to print per person', default=10, type=int)
    parser.add_argument('-w', '--words-to-match', help='Words to match (separated by commas)', default="")
    parser.add_argument('-v', '--verbose', help='Additional info', action='count', default=0)
    parser.add_argument('-a', '--average-vocab', help='Print average vocabulary at the end', action='store_true')

    args = parser.parse_args()

    if (args.input != None):
        master_folder = args.input
        save_dir(master_folder)
    else:
        try:
            master_folder = load_dirs()[-1]
        except IndexError:
            print("No Facebook data folder found. Please run:\n\tpython analyzer.py -i <path to folder>\n")
            print("first to remember the Facebook data folder.")
            sys.exit(1)

    master_folder = os.path.join(master_folder, "messages", "inbox")

    if not os.path.exists(master_folder):
        print("Folder does not exist:", master_folder)
        print("Error: Facebook data folder not found. Try running:\n\tpython analyzer.py -i <path to folder>")
        print("Remember to choose the correct folder, it must include the 'messages' folder inside it!")
        exit()

    vocab_analyzer = VocabularyAnalyzer()

    messages_count = {}

    words_to_match = args.words_to_match.split()
    if (args.verbose > 0):
        print("Words to match:", words_to_match)

    for conversation_folder in os.listdir(master_folder):
        conversation_folder = os.path.join(master_folder, conversation_folder)
        messages = read_folder(conversation_folder)
        if (args.verbose > 1):
            print_fb(messages[0]["title"])
        for message_file in messages:
            for message in message_file["messages"]:
                vocab_analyzer.add_message_to_vocabulary(message,words_to_match)

                if "content" in message and message["type"] == "Generic":
                    sender = decode_fb(message["sender_name"])
                    if sender not in messages_count:
                        messages_count[sender] = 0
                    messages_count[sender] += 1

    vocab_analyzer.calculate_average_vocab()

    print("--------------------")
    print("DONE")
    print("--------------------")

    sorted_messages_count = sorted(messages_count.items(), key=lambda x: x[1], reverse=True)

    n_senders = args.top_senders
    n_words = args.number_of_words

    if (args.person != None):
        for sender in args.person:
            print(sender, messages_count[sender])
            print_vocab(vocab_analyzer.get_vocab(sender), n_words)
            print("Characteristic words:")
            print_vocab(vocab_analyzer.characteristic_vocab(sender), n_words, vocab_analyzer.get_vocab(sender), vocab_analyzer.get_vocab())

        
    for sender, count in sorted_messages_count[:n_senders]:
        print(sender, count)
        print_vocab(vocab_analyzer.characteristic_vocab(sender), n_words, vocab_analyzer.get_vocab(sender), vocab_analyzer.get_vocab())

    if args.average_vocab:
        print("")
        print("Total vocabulary:")
        print_vocab(vocab_analyzer.get_vocab(), n_words)