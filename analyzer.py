import os
#import JSON library
import json
import sys

from numpy import size
from loader import read_folder

master_folder = os.path.join("messages", "inbox")

def print_fb(string):
    print(string.encode('latin1').decode('utf8'))

# create an empty dict
all_vocabularies = {}
total_words = {}

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
                    if sender in total_words:
                        total_words[sender] += 1
                    else:
                        total_words[sender] = 1

def print_vocab(vocabulary, n=100, overall_vocabulary=None):
    print("Vocabulary size:" + str(len(vocabulary)))
    i = 0
    for word in sorted(vocabulary, key=vocabulary.get, reverse=True)[:n]:
        i += 1
        if overall_vocabulary == None:
            print(str(i)+".", word, vocabulary[word])
        else:
            print(str(i)+".", word, vocabulary[word], overall_vocabulary[word])
    
def normalize_vocab(vocabulary, bias=0):
    sum = 0.0
    for word in vocabulary:
        sum += vocabulary[word] + bias

    normalized = {}
    for word in vocabulary:
        normalized[word] = (vocabulary[word] + bias) * 100/sum
    return normalized

def relative_vocab(vocabulary, master_vocabulary):
    relative_vocabulary = {}
    for word in vocabulary:
        relative_vocabulary[word] = vocabulary[word]/ master_vocabulary[word]
    return relative_vocabulary

# for sender in all_vocabularies:
#     print(sender)
#     print_vocab(all_vocabularies[sender], 10)
#     print("")

vocabulary_sizes = {}
for sender in all_vocabularies.keys():
    vocabulary_sizes[sender] = len(all_vocabularies[sender])

# print senders from largest vocabulary to smallest
sorted_vocabularies = sorted(vocabulary_sizes, key=vocabulary_sizes.get, reverse=True)

i = 0
magnitude_order = float("inf")

average_vocabulary = {}
for sender in sorted_vocabularies:
    if len(str(vocabulary_sizes[sender])) < magnitude_order:
        magnitude_order = len(str(vocabulary_sizes[sender]))
    i += 1
    # print(str(i)+".", sender, vocabulary_sizes[sender])
    for word in all_vocabularies[sender]:
        if word in average_vocabulary:
            average_vocabulary[word] += all_vocabularies[sender][word]/total_words[sender]*magnitude_order
        else:
            average_vocabulary[word] = all_vocabularies[sender][word]/total_words[sender]*magnitude_order

average_vocabulary_normalized = normalize_vocab(average_vocabulary, 0.01)

for sender in ["your name", "your friend's name"]:
    print(sender)
    print_vocab(relative_vocab(normalize_vocab(all_vocabularies[sender]), average_vocabulary_normalized), 100, all_vocabularies[sender])


# print("Average vocabulary:")
# print_vocab(average_vocabulary, 100)