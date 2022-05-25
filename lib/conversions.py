import datetime, os

from lib.loader import save_dir, load_dirs

def print_fb(string):
    print(decode_fb(string))

def timestamp_to_date_string(timestamp):
    #hour and date
    return datetime.datetime.fromtimestamp(timestamp/1000).strftime('%Y-%m-%d %H:%M:%S')

def decode_fb(string):
    return string.encode('latin1').decode('utf8')

def print_message(message):
    print(timestamp_to_date_string(message["timestamp_ms"]))
    print_fb(message["sender_name"])
    if "content" in message:
        print_fb(message["content"])
    if "photos" in message:
        print(message["photos"])
    if "videos" in message:
        print(message["videos"])
    print("")

def parse_folder(input, script_name):
    if (input != None):
        master_folder == input
        save_dir(master_folder)
    else:
        try:
            master_folder = load_dirs()[-1]
        except IndexError:
            print("No Facebook data folder found. Please run:\n\tpython " + script_name+  " -i <path to folder>\n")
            print("first to remember the Facebook data folder.")
            exit()
    
    master_folder = os.path.join(master_folder, "messages", "inbox")

    if not os.path.exists(master_folder):
        print("Folder does not exist:", master_folder)
        print("Error: Facebook data folder not found. Try running:\n\tpython " + script_name +  " -i <path to folder>")
        print("Remember to choose the correct folder, it must include the 'messages' folder inside it!")
        exit()
    
    return master_folder