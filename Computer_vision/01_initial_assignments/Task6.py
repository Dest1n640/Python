word1 = input("Input the first word: ")
word2 = input("Input the second word: ")

Na = ""
Nb = ""
Nc = ""


def amount_of_elements(word, N):
    for i in word:
        if i not in N:
            N += i
    return N


Na = amount_of_elements(word1, Na)
Nb = amount_of_elements(word2, Nb)

for i in Na:
    for j in Nb:
        if i == j:
            Nc += i

formula = len(Nc) / (len(Na) + len(Nb) - len(Nc))
print(f"T = {formula}")
