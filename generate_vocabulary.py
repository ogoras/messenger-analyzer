import argparse, os, sys

from vocabulary import VocabularyAnalyzer
from loader import read_folder, load_dirs, save_dir
from lib import print_fb, decode_fb
from word_finder import WordFinder

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate a vocabulary data file')
    parser.add_argument('-i', '--input', help='Your Facebook data folder (should contain the folder "messages" inside it)')
    parser.add_argument('-v', '--verbose', help='Additional info', action='count', default=0)
    parser.add_argument('--vocab', help='Generate vocabulary file', action='store_true')
    parser.add_argument('-w', '--words-to-match', help='Words to match')

    args = parser.parse_args()

    if (args.input != None):
        master_folder = args.input
        save_dir(master_folder)
    else:
        try:
            master_folder = load_dirs()[-1]
        except IndexError:
            print("No Facebook data folder found. Please run:\n\tpython " + sys.argv[0] +  " -i <path to folder>\n")
            print("first to remember the Facebook data folder.")
            exit()
    
    master_folder = os.path.join(master_folder, "messages", "inbox")

    if not os.path.exists(master_folder):
        print("Folder does not exist:", master_folder)
        print("Error: Facebook data folder not found. Try running:\n\tpython " + sys.argv[0] +  " -i <path to folder>")
        print("Remember to choose the correct folder, it must include the 'messages' folder inside it!")
        exit()

    vocab_analyzer = None
    if(args.vocab):
        vocab_analyzer = VocabularyAnalyzer()

    word_finder = None
    if(args.words_to_match != None):
        word_finder = WordFinder(args.words_to_match.split(), args.verbose)

    for conversation_folder in os.listdir(master_folder):
        conversation_folder = os.path.join(master_folder, conversation_folder)
        messages = read_folder(conversation_folder)
        # if (args.verbose > 1):
        #     print_fb(messages[0]["title"])
        for message_file in messages:
            for message in message_file["messages"]:
                if(args.vocab):
                    vocab_analyzer.add_message_to_vocabulary(message)
                if(word_finder != None):
                    word_finder.search_message(message)

    if(args.vocab):
        vocab_analyzer.calculate_average_vocab()
        vocab_analyzer.save_vocab()
    
    if(word_finder != None):
        word_finder.print_results()
