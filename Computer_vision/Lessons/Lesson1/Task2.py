word = input("Input the  word: ")

vowels = ["a", "e", "i", "o", "u"]
consonants = len(word)
amount = 0

for i in word:
    for j in vowels:
        if i == j:
            amount += 1

print(f"Number of vowels == {amount}, number of consonants == {consonants - amount}")
