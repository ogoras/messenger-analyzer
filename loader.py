import os
import json

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

def load_dirs():
    if not os.path.exists("saved_dirs.json"):
        return []
    with open("saved_dirs.json", "r") as f:
        return json.load(f)

def save_dir(dir_path):
    dir_list = load_dirs()

    if dir_path in dir_list:
        #remove it
        dir_list.remove(dir_path)

    dir_list.append(dir_path)

    with open("saved_dirs.json", "w") as f:
        json.dump(dir_list, f)

def save_vocab(vocab):
    with open("vocab.json", "w") as f:
        json.dump(vocab, f)

def load_vocab():
    if not os.path.exists("vocab.json"):
        return {}
    with open("vocab.json", "r", encoding='utf-8') as f:
        return json.load(f)