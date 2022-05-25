def process_word(word):
    word = word.strip('.,!?;:*()[]{}<>…"\'/\\”“')
    return word.lower()