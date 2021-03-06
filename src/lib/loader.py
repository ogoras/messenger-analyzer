import os
import json

from .conversions import print_fb
from ..filtering.filter import EmptyFilter, Filter

#TYPES:
# Subscribe - someone joined (for group chats)
# Unsubscribe - someone left (for group chats)
# Share - someone shared a link
# Call - someone called (video or audio)
# Generic - everything else

# Generic messages can have different attributes (and sometimes more than one):
#   "content" - text
#   "photos" - photos
#   "videos" - videos
#   "sticker" - stickers
#   "audio_files" - voice messages and the like
#   "files" - other attached files
#   "gifs" - gifs
#   "reactions" - reactions : {"reaction": "some emoji", "actor": "some user"}

# THREAD TYPES:
# RegularGroup - group chat
# Regular - one on one

def parse_folder(input, script_name):
    if (input != None):
        master_folder = input
        save_dir(master_folder)
    else:
        try:
            master_folder = load_dirs()[-1]
        except IndexError:
            print("No Facebook data folder found. Please run:\n\tpython " + script_name +  " -i <path to folder>\n")
            print("first to remember the Facebook data folder.")
            exit()
    
    master_folder = os.path.join(master_folder, "messages")

    if not os.path.exists(master_folder):
        print("Folder does not exist:", master_folder)
        print("Error: Facebook data folder not found. Try running:\n\tpython " + script_name +  " -i <path to folder>")
        print("Remember to choose the correct folder, it must include the 'messages' folder inside it!")
        exit()
    
    return master_folder


def read_folder(conversation_folder):
    threads = []
    for filename in os.listdir(conversation_folder):
        filename = os.path.join(conversation_folder, filename)

        #check if it's a JSON file
        if os.path.isfile(filename) and filename.endswith(".json"):
            #load JSON
            with open(filename, "r") as f:
                threads.append(json.load(f))

    return threads

def gen_messages(master_folder, filter : Filter = EmptyFilter(), verbose=False):

    for subfolder in ["archived_threads", "filtered_threads", "inbox", "message_requests"]:
        if not os.path.isdir(os.path.join(master_folder, subfolder)):
            continue
        for conversation_folder in os.listdir(os.path.join(master_folder, subfolder)):
            threads = read_folder(os.path.join(master_folder, subfolder, conversation_folder))
            if (verbose):
                print_fb(threads[0]["title"])
            for thread in threads:
                for message in thread["messages"]:
                    if (filter.filter(subfolder, conversation_folder, thread, message)):
                        yield (subfolder, conversation_folder, thread, message)

def load_dirs():
    if not os.path.exists(os.path.join("saved", "saved_dirs.json")):
        return []
    with open(os.path.join("saved", "saved_dirs.json"), "r") as f:
        return json.load(f)

def save_dir(dir_path):
    dir_list = load_dirs()

    if dir_path in dir_list:
        #remove it
        dir_list.remove(dir_path)

    dir_list.append(dir_path)

    with open(os.path.join("saved", "saved_dirs.json"), "w") as f:
        json.dump(dir_list, f)

class MyEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__ 

def save(object, filename):
    filename = os.path.join("saved", filename)
    with open(filename, "w") as f:
        json.dump(object, f, cls=MyEncoder)

def load(filename):
    filename = os.path.join("saved", filename)
    if not os.path.exists(filename):
        return {}
    with open(filename, "r", encoding='utf-8') as f:
        return json.load(f)