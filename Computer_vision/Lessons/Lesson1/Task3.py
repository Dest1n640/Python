filename = "words.txt"
with open(filename, "r", encoding="utf-8") as file:
    text = file.read()
    words = text.split()
    if words:
        longest_word = max(words, key=len)
        print(f"The longest word in file '{filename}' is: {longest_word}")
    else:
        print(f"Could not find any words in file '{filename}'")
