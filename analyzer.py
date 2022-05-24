import os

from loader import read_folder
from vocabulary import print_vocab, VocabularyAnalyzer

def print_fb(string):
    print(string.encode('latin1').decode('utf8'))

if __name__ == "__main__":
    master_folder = os.path.join("messages", "inbox")

    vocab_analyzer = VocabularyAnalyzer()

    for conversation_folder in os.listdir(master_folder):
        conversation_folder = os.path.join(master_folder, conversation_folder)
        messages = read_folder(conversation_folder)
        print_fb(messages[0]["title"])
        for message_file in messages:
            for message in message_file["messages"]:
                vocab_analyzer.add_message_to_vocabulary(message)

    vocab_analyzer.calculate_average_vocab()

    print("--------------------")
    print("DONE")
    print("--------------------")

    for sender in ["your name", "your friend's name"]:
        print(sender)
        print_vocab(vocab_analyzer.characteristic_vocab(sender), 100, vocab_analyzer.get_vocab(sender))

    print("Average vocabulary:")
    print_vocab(vocab_analyzer.get_vocab(), 100)