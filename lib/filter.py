# Okay, how many ways are there to filter the data?
# 1. sender
#   1a. sender first name
#   1b. sender last name
# 2. timestamp
#   2a. timestamp range
#   2b. days of the week
#   2c. days of the year
#   2d. hours of the day
#   2e. ...
# 3. subfolder (inbox, archived_threads, filtered_threads)
# 4. type (generic, subscribe, unsubscribe, share, call)
#   4a. Generic:
#       4a1. filter by attributes present (content, photos, videos, sticker, audio_files, files, gifs, reactions)
#   4b. ...
# 5. conversation_folder (conversation_id?)
# 6. thread_type (regular, group)
# 7. thread participants

class Filter:
    def __init__(self):
        pass
    
    #TODO: unmock
    def filter(self, subfolder, conversation_folder, thread, message):
        return True