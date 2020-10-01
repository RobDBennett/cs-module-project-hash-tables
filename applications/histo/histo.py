"""
These are all garbage methods because I did this out of order rather than starting
with Word_Count which would have made the process infinitely easier.
import re

text = open("robin.txt", "r")
d = dict()

for line in text:
    line = line.strip()
    line = line.lower()
    line = line.replace('|', "")
    re.sub('"|:|;|,|.|-|+|=|/|\|[|]|{|}|(|)|*|^|&', "", line)
    words = line.split(" ")
    #words = words.translate({ord(i): None for i in '":;,.-+=/\|[]{ }()*^&'})
    for word in words:
        if word in d:
            d[word] = d[word] + 1
        else:
            d[word] = 1

for key in list(d.keys()):
    print(key, ":", d[key])

text = open("robin.txt", "r")
corpus= {}
obnoxious_chars = ['"', ':', ';', ',', '.', '-', '+', '=', '/', "\\", '|', '[', ']', '{', '}', '(', ')', '*', '^', '&']

def word_count(s, chars):
    s2 = ''.join(c.lower() for c in s if not c in chars)
    for word in s2.split():
        corpus[word] = corpus[word] + 1 if word in corpus else 1
    return corpus

def sort_by(t):
    return t[1]

word_count(text, obnoxious_chars)
print(corpus)
items = list(corpus.items())
print(items.sort(key=sort_by, reverse=True))


text = open("robin.txt", "r")
text = text.read()
text = text.lower()
to_remove = ['"', ':', ';', ',', '.', '-', '+', '=', '/', "\\", '|', '[', ']', '{', '}', '(', ')', '*', '^', '&', "'", '!', '?', "''"]
space = " "
word_count = {}
word = ""
for x in to_remove:
    text = text.replace(x, '')

for word in text:
    if word in word_count:
        word_count[word] += 1
    else:
        word_count[word] = 1

print(word_count)


text = open("robin.txt", "r")
to_remove = ['"', ':', ';', ',', '.', '-', '+', '=', '/', "\\", '|', '[', ']', '{', '}', '(', ')', '*', '^', '&', "'", '!', '?', "''"]
space = " "
word_count = {}
word = ""

for character in text.read().lower():
    if character.split() in to_remove:
        continue
    if character == space or character == "\n":
        
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1
        word = ""
    else:
        word += character
#print(word_count)
#sorted_word_count = sorted(word_count.items(), reverse=True, key= lambda item: item[0])
sorted_word_count = sorted(word_count.items(), key=lambda item: item[1])
sorted_word_count = sorted_word_count[::-1]
print(sorted_word_count)

for word in sorted_word_count:
    if word[1] > 5:
        histogram += word[0]
        for i in range(0, items - len(histogram)):
            histogram += " "
        for i in range(0, word[1]):
            histogram += "#"
        print(histogram)
        histogram = ""
"""
text = open("robin.txt", "r") #Read in the txt file.
text = text.read() #Convert to a read() format.
def word_count(s): #Function from Word_Count. I added a few punctuations to it.
    dict = {} #Create a dictionary.
    for word in s.split(): #Split the input text into words as they encounter white space.
        word = word.lower() #Change each word to lowercase.
        drop_char = '":;,.-+=/\|[]{}()*^&?!' #The list of BS characters to nix. NOT A LIST.
        for character in word: #Iterate over each character of the broken up words.
            if character in drop_char: #If any of the characters in the BS are present...
                word = word.replace(character,"") #Replace them with nothing.
        if word in dict: #Check to see if the word exists in the dictionary.
            dict[word] += 1 #If so, add 1
        elif word != '': #As long as the word isn't empty- this was added because I couldn't find another way.
            dict.update({word:1}) #Set starting value to 1.
    return dict #Returns your dictionary.

corpus = word_count(text) #Run your text through the word counter.
alpha_sorted_corpus = sorted(corpus.items(), reverse=True,key=lambda item: item[0]) #Sort alphabetically (key)
sorted_corpus = sorted(alpha_sorted_corpus, key= lambda item:item[1]) #Sort numerically (Value)
sorted_corpus = sorted_corpus[::-1] #This was added to ensure the order is correct. Reversing the numerical sort failed.

histogram = "" #Start a blank place holder.
items = 15 #This is the number of spaces between the word and when their hashes start.

for word in sorted_corpus: #Iterate over each word in the heavily sorted dictionary.
    if word[1] > 5: #Because this gets cartoony, only take the highest counted words.
        histogram += word[0] #Adds the word (key) to the place holder.
        for i in range(0, items - len(histogram)): #Takes the difference between the size of the word and the space
            histogram += " " #Adds spaces equal to the difference between the size of the word and the arbitary number
        for i in range(0, word[1]): #Iterates over the count (value)
            histogram += "#" #Adds a hash for each time it appears.
        print(histogram) #Print the current histogram.
        histogram = "" #Reset placeholder to repeat process.

#print("%12s %s" % (item[0], item[1] * '#"))