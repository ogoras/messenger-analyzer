import datetime

def print_fb(string):
    print(string.encode('latin1').decode('utf8'))

def timestamp_to_date_string(timestamp):
    #hour and date
    return datetime.datetime.fromtimestamp(timestamp/1000).strftime('%Y-%m-%d %H:%M:%S')

def decode_fb(string):
    return string.encode('latin1').decode('utf8')

def print_message(message):
    print(timestamp_to_date_string(message["timestamp_ms"]))
    print(message["sender_name"])
    if "content" in message:
        print(message["content"])
    if "photos" in message:
        print("photos")
    if "videos" in message:
        print("videos")
    print("")