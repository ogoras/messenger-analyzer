import os, sys

from loader import read_folder
from vocabulary import print_vocab, VocabularyAnalyzer
from lib import print_fb

if __name__ == "__main__":
    master_folder = os.path.join("messages", "inbox")

    vocab_analyzer = VocabularyAnalyzer()

    messages_count = {}
    words_to_match = []
    if len(sys.argv) > 3:
        words_to_match = sys.argv[3].split()
        print(words_to_match)

    for conversation_folder in os.listdir(master_folder):
        conversation_folder = os.path.join(master_folder, conversation_folder)
        messages = read_folder(conversation_folder)
        # print_fb(messages[0]["title"])
        for message_file in messages:
            for message in message_file["messages"]:
                vocab_analyzer.add_message_to_vocabulary(message,words_to_match)

                if "content" in message and message["type"] == "Generic":
                    sender = message["sender_name"].encode('latin1').decode('utf8')
                    if sender not in messages_count:
                        messages_count[sender] = 0
                    messages_count[sender] += 1

    vocab_analyzer.calculate_average_vocab()

    print("--------------------")
    print("DONE")
    print("--------------------")

    sorted_messages_count = sorted(messages_count.items(), key=lambda x: x[1], reverse=True)

    n_senders = 10
    n_words = 10
    if len(sys.argv) > 1:
        n_senders = int(sys.argv[1])
        if len(sys.argv) > 2:
            n_words = int(sys.argv[2])
        
    for sender, count in sorted_messages_count[:n_senders]:
        print(sender, count)
        print_vocab(vocab_analyzer.characteristic_vocab(sender), n_words, vocab_analyzer.get_vocab(sender), vocab_analyzer.get_vocab())

    # print("")
    # print("Average vocabulary:")
    # print_vocab(vocab_analyzer.get_vocab(), 100)