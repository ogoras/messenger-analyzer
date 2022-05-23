import os
#import JSON library
import json
from loader import read_folder

master_folder = os.path.join("messages", "inbox")

def print_fb(string):
    print(string.encode('latin1').decode('utf8'))

# create an empty dict
all_vocabularies = {}

for conversation_folder in os.listdir(master_folder):
    conversation_folder = os.path.join(master_folder, conversation_folder)
    messages = read_folder(conversation_folder)
    print_fb(messages[0]["title"])
    for message_file in messages:
        for message in message_file["messages"]:
            if "content" in message and message["type"] == "Generic":
                sender = message["sender_name"].encode('latin1').decode('utf8')
                if sender not in all_vocabularies:
                    all_vocabularies[sender] = {}
                vocabulary = all_vocabularies[sender]

                content = message["content"].encode('latin1').decode('utf8')
                for word in content.split():
                    word = word.lower()
                    if word in vocabulary:
                        vocabulary[word] += 1
                    else:
                        vocabulary[word] = 1

def print_vocab(vocabulary, n=100):
    print("Vocabulary size:" + str(len(vocabulary)))
    i = 0
    for word in sorted(vocabulary, key=vocabulary.get, reverse=True)[:n]:
        i += 1
        print(str(i)+".", word, vocabulary[word])
    
for sender in all_vocabularies:
    print(sender)
    print_vocab(all_vocabularies[sender], 10)
    print("")
    vocabulary_sizes = {}
    for sender in all_vocabularies.keys():
        vocabulary_sizes[sender] = len(all_vocabularies[sender])

# print senders from largest vocabulary to smallest
sorted_vocabularies = sorted(vocabulary_sizes, key=vocabulary_sizes.get, reverse=True)
print("Sorted vocabularies:")
i = 0
for sender in sorted_vocabularies:
    i += 1
    print(str(i)+".", sender, vocabulary_sizes[sender])

print ("Total vocabulary:", len(all_vocabularies.keys()))