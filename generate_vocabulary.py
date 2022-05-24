import argparse, os, sys

from vocabulary import VocabularyAnalyzer
from loader import read_folder, load_dirs, save_dir
from lib import print_fb, decode_fb

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate a vocabulary data file')
    parser.add_argument('-i', '--input', help='Your Facebook data folder (should contain the folder "messages" inside it)')
    parser.add_argument('-v', '--verbose', help='Additional info', action='count', default=0)

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

    vocab_analyzer = VocabularyAnalyzer()

    for conversation_folder in os.listdir(master_folder):
        conversation_folder = os.path.join(master_folder, conversation_folder)
        messages = read_folder(conversation_folder)
        if (args.verbose > 1):
            print_fb(messages[0]["title"])
        for message_file in messages:
            for message in message_file["messages"]:
                vocab_analyzer.add_message_to_vocabulary(message)

    vocab_analyzer.calculate_average_vocab()

    vocab_analyzer.save_vocab()
