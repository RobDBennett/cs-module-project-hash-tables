import random
import itertools
# Read in all the words in one go
with open("input.txt") as f:
    words = f.read()

# TODO: analyze which words can follow other words
split_words = words.split()
dict = {}

for i, word in enumerate(split_words):
    if i+1 < len(split_words):
        if word not in dict:
            dict[word] = [split_words[i+1]]
        else:
            dict[word].append(split_words[i+1])

start_word = []
stop_word = []

for word in split_words:
    if word[0].isupper():
        start_word.append(word)
    if word[0] == '"':
        start_word.append(word)
    if word.endswith(('"', "!", "?", ".")):
        stop_word.append(word)

for i in range(5):
    print(f'Sentence {i+1}:')
    word = random.choice(start_word)
    space = " "
    sentence = word + space
    new_word = word
    while new_word not in stop_word:
        new_list = dict[new_word]
        new_word = random.choice(new_list)
        sentence = sentence + new_word + space
    print(sentence)
