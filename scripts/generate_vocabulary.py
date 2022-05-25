import argparse, os, sys

from vocab.vocabulary_analyzer import VocabularyAnalyzer
from lib.loader import read_folder
from lib.conversions import print_fb, parse_folder

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate a vocabulary data file')
    parser.add_argument('-i', '--input', help='Your Facebook data folder (should contain the folder "messages" inside it)')
    parser.add_argument('-v', '--verbose', help='Additional info', action='count', default=0)

    args = parser.parse_args()

    master_folder = parse_folder(args.input, sys.argv[0])

    vocab_analyzer = VocabularyAnalyzer()

    #TODO: turn this into a generator :D
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
