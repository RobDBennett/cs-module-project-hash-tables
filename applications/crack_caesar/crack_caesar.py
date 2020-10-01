# Use frequency analysis to find the key to ciphertext.txt, and then
# decode it.

text = open("ciphertext.txt", "r") #Load in the data
text = text.read() #Make it readable.

def char_count(s): #Create a cleaner/counter function.
    dict = {} #Start a dictionary
    for char in s: #Iterate through each character (similar to word_count, but no split())
        char = char.lower() #This is ultimately unnecessary, but I didn't realize that at the time. Remove.
        drop_char = '":;,.-+=/\|[]{}()*^&!-?1' #There are a bunch of odd characters.
        if char in drop_char: #Eliminates weird characters
            char = char.replace(char,"")
        if char == " ": #Eliminates white space
            char = char.replace(char, "")
        if char == "'": #Eliminates edgecase
            char = char.replace(char, "")
        if char == "—": #Edgecase
            char = char.replace(char, "")
        if char == "\n": #Edgecase
            char = char.replace(char,"")
        if char in dict: #Checks if the character is already counted
            dict[char] += 1 #Adds one to the total.
        elif char != '': #If its not in there
            dict.update({char:1}) #Set to 1
    return dict #Return the dictionary.

chars = char_count(text) #Run the document through the counter.

sorted_chars = sorted(chars.items(), reverse=True, key=lambda item: item[1]) #Sort by value, most at the top.

#This coded list is taken from the readme. I foolishly did a .lower() so couldn't just use it, but replace with lower. LIKE A FOOL.
coded = ['e', 't', 'a', 'o', 'h', 'n', 'r', 'i', 's', 'd', 'l', 'w', 'u', 'g', 'f', 'b', 'm', 'y', 'c', 'p', 'k','v','q','j','x','z']

def decipher(clean, coded): #Function to take the character count dictionary and replace the value with the proper letters.
    the_code = coded #I didn't want to change the list in place, so set to new variable.
    decoded = {} #Set a dictionary for the new values. Could alter in place as well.
    for item in clean: #Loads previous dictionary into the new one.
        decoded[item[0]] = item[1]
    for item in decoded: #Goes through the new dictionary.
        decoded[item] = the_code[0] #replaces the value of dictionary item with 1st item in code list
        the_code.pop(0) #Delete first item in the code list.
    return decoded #Return the new dictionary of the encoded letters and the proper letters as key/value pairs.

cipher = decipher(sorted_chars, coded) #Run cleaned, counted and sorted dict and code through function

def decoded(s,cipher): #Function to translate text.
    s = s.lower() #Because I am an idiot.
    answer = "" #Start an empty string. NOT A LIST.
    for char in s: #Iterate through each character of the original text.
        if char in cipher.keys(): #If that character also exists as a KEY in the decoder library.
            to_replace = cipher.get(char) #Cast the current character to a variable (the value of that key)
            to_replace = str(to_replace) #Ensure its a string.
            answer = answer + to_replace #Add that character to the existing string.
        else: #If the character isn't in the decoder, that means its special, punctuation, space, etc
            answer = answer + char #Keep whatever that character is and add it to the string.
    return answer.upper() #Make it uppercase so that it's the same as the original.

answer = decoded(text, cipher) #Run the original text and cipher through the function.
print(answer) #Print returned answer.
