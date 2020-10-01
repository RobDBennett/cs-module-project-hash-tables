def no_dups(s):
    clean = []
    if s == "":
        return ""
    else:
        for word in s.split():
            if word in clean:
                continue 
            else:
                clean.append(word)
    answer = ""
    for word in clean:
        answer += word
        answer += " "
    return answer.strip()

if __name__ == "__main__":
    print(no_dups(""))
    print(no_dups("hello"))
    print(no_dups("hello hello"))
    print(no_dups("cats dogs fish cats dogs"))
    print(no_dups("spam spam spam eggs spam sausage spam spam and spam"))