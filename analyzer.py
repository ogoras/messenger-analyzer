import os
#import JSON library
import json
from loader import read_folder

master_folder = os.path.join("messages", "inbox")

def print_fb(string):
    print(string.encode('latin1').decode('utf8'))

for conversation_folder in os.listdir(master_folder):
    conversation_folder = os.path.join(master_folder, conversation_folder)
    messages = read_folder(conversation_folder)
    print_fb(messages[0]["title"])



