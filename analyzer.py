import os
#import JSON library
import json

master_folder = os.path.join("messages", "inbox")

def print_fb(string):
    print(string.encode('latin1').decode('utf8'))

def read_folder(conversation_folder):
    messages = []
    for filename in os.listdir(conversation_folder):
        filename = os.path.join(conversation_folder, filename)

        #check if it's a JSON file
        if os.path.isfile(filename) and filename.endswith(".json"):
            #load JSON
            with open(filename, "r") as f:
                messages.append(json.load(f))

    return messages

for conversation_folder in os.listdir(master_folder):
    conversation_folder = os.path.join(master_folder, conversation_folder)
    messages = read_folder(conversation_folder)
    print(conversation_folder)
    print_fb(messages[0]["title"])