def word_count(s):
    dict = {}
    for word in s.split():
        word = word.lower()
        drop_char = '":;,.-+=/\|[]{}()*^&'
        for character in word:
            if character in drop_char:
                word = word.replace(character,"")
        if word in dict:
            dict[word] += 1
        elif word != '':
            dict.update({word:1})
    print(f'Cache: {dict}')
    return dict

if __name__ == "__main__":
    print(word_count(""))
    print(word_count("Hello"))
    print(word_count('Hello, my cat. And my cat doesn\'t say "hello" back.'))
    print(word_count('This is a test of the emergency broadcast network. This is only a test.'))