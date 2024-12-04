import random
import nltk
count = 0
nltk.download("words")
from nltk.corpus import words

word_list = words.words()

random_word = random.choice(word_list)
print(random_word)

print(f"in the word {len(random_word)} letters")

my_word = input("guess the word - ")
while random_word != my_word:
    my_word = input("guess the word - ")
    count += 1
    for ind, i in enumerate(my_word):
        for ind1, q in enumerate (random_word):
            if ind == ind1 and i == q:
                print(f"you guess the letter in the position {ind+1}")
                continue
    if random_word == my_word:
        print("you guess")
    elif count == 5:
        print("you lose")   
        break