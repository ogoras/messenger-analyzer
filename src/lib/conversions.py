import datetime

def print_fb(string):
    print(decode_fb(string))

def timestamp_to_date_string(timestamp):
    #hour and date
    return datetime.datetime.fromtimestamp(timestamp/1000).strftime('%Y-%m-%d %H:%M:%S')

def date_to_timestamp(year, month=1, day=1, hour=0, minute=0, second=0):
    return datetime.datetime(year, month, day, hour, minute, second).timestamp() * 1000

def decode_fb(string : str):
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