import random
import itertools
# Read in all the words in one go
with open("input.txt") as f:
    words = f.read()

# TODO: analyze which words can follow other words
# I feel like this is a modified word count. 

split_words = words.split()
dict = {}

for i, word in enumerate(split_words):
    if i+1 < len(split_words):
        if word not in dict:
            dict[word] = [split_words[i+1]]
        else:
            dict[word].append(split_words[i+1])
#print(dict)

start_word = []
middle_word = []
stop_word = []

for word in split_words:
    if word[0].isupper():
        start_word.append(word)
    if word[0] == '"':
        start_word.append(word)
    if word.endswith(('"', "!", "?", ".")):
        stop_word.append(word)

for word in split_words:
    if word not in start_word:
        if word not in stop_word:
            middle_word.append(word)
#print(middle_word)

# TODO: construct 5 random sentences
for i in range(5):
    print(f'Sentence {i+1}:')
    word = random.choice(start_word)
    space = " "
    sentence = word + space
    new_word = word
    for _ in range(random.randint(1,8)):
        new_list = dict[new_word]
        new_word = random.choice(new_list)
        sentence = sentence + new_word + space
        if new_word in stop_word:
            break
    while new_word not in stop_word:
        new_list = dict[new_word]
        new_word = random.choice(new_list)
        sentence = sentence + new_word + space
    print(sentence)


"""
    for _ in range(random.randint(1,8)):
        new_word = random.choice(dict)
        if new_word in start_word:
            new_word = random.choice(dict)
        elif new_word in stop_word:
            new_word = random.choice(dict)
        word = word + new_word
    last_word = random.choice(stop_word)
    word = word + last_word
    print(word)
    


This works, but I don't think its looking things up in the dictionaries correctly.
starting_chars= 'ABCDEFGHIJKLMNOPQRSTUVWXYZ"'
ending_chars = '.?!'
word_dict = {}
index = -1
word_array = words.split()
start = "starting_words"
previous_word = word_array[0]
word_dict[start] = []
for word in word_array:
    if word[-1] == '"':
        word = word.replace('"', "")
    if word[-1] == ':':
        word = word.replace(':', "")
    if word[0] == '(':
        word = word.replace('(', "")
    if word[-1] == ')':
        word = word.replace(')', "")
    if word[0] == '"' and word[1] in starting_chars:
        word_dict[start].append(word)
    elif word[0] in starting_chars:
        word_dict[start].append(word)
    if word_dict.__contains__(word) is False:
        word_dict.setdefault(word, [])
    if index >= 0:
        word_dict[previous_word].append(word)
        previous_word = word
    index += 1

sentences = []

while len(sentences) != 5:
    starting_word = random.choice(word_dict[start])
    word = starting_word
    sentence = f"{starting_word} "
    while word[-1] not in ending_chars:
        word = random.choice(word_dict[word])
        if word in word_dict[start]:
            while word in word_dict[start]:
                word = random.choice(word_dict[word])
        sentence += f"{word} "
    sentences.append(sentence.rstrip())

for sentence in sentences:
    if sentence[0] == '"' and sentence[-1] != '"':
        sentence += '"'
    print(sentence, end="\n\n")
"""