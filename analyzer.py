import os, sys

from loader import read_folder
from vocabulary import print_vocab, VocabularyAnalyzer
from lib import decode_fb

if __name__ == "__main__":
    master_folder = "."
    if len(sys.argv) > 1:
        master_folder = sys.argv[1]
        # convert single backslashes to double backslashes

    master_folder = os.path.join(master_folder, "messages", "inbox")

    if not os.path.exists(master_folder):
        print("Folder does not exist:", master_folder)
        print("Error: Facebook data folder not found. Try running:\n\tpython analyzer.py <path to folder>")
        print("Remember to choose the correct folder, it must include the 'messages' folder inside it!")
        sys.exit(1)

    vocab_analyzer = VocabularyAnalyzer()

    messages_count = {}
    words_to_match = []
    if len(sys.argv) > 5:
        words_to_match = sys.argv[5].split()
        print(words_to_match)

    for conversation_folder in os.listdir(master_folder):
        conversation_folder = os.path.join(master_folder, conversation_folder)
        messages = read_folder(conversation_folder)
        # print_fb(messages[0]["title"])
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

    n_senders = 10
    n_words = 10
    if len(sys.argv) > 2:
        #check if it's integer
        n_senders = int(sys.argv[2])
        if len(sys.argv) > 3:
            n_words = int(sys.argv[3])

    if len(sys.argv) > 4:
        sender = sys.argv[4]
        print(sender, messages_count[sender])
        print_vocab(vocab_analyzer.get_vocab(sender), n_words)
        print_vocab(vocab_analyzer.characteristic_vocab(sender), n_words, vocab_analyzer.get_vocab(sender), vocab_analyzer.get_vocab())

        
    for sender, count in sorted_messages_count[:n_senders]:
        print(sender, count)
        print_vocab(vocab_analyzer.characteristic_vocab(sender), n_words, vocab_analyzer.get_vocab(sender), vocab_analyzer.get_vocab())

    # print("")
    # print("Total vocabulary:")
    # print_vocab(vocab_analyzer.get_vocab(), 100)