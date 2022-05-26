def process_word(word):
    word = word.strip('.,!?;:*()[]{}<>…"\'/\\”“„-')
    return word.lower()

def match_words(pattern, word, match="whole"):
    if match == "whole":
        return pattern == word
    elif match == "left":
        return word.startswith(pattern)
    elif match == "right":
        return word.endswith(pattern)
    elif match == "contains":
        return pattern in word
    else:
        raise Exception("Unknown match type: " + match)