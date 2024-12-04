class Word:
    def __init__(self, word):
        self.word = word

    def __repr__(self):
        return self.word

    def __str__(self):
        self.word = self.word.lower()
        return self.word.capitalize()

    def __eq__(self, other):
        if isinstance(other, Word):
            return f"Are the words equal? - {len(self.word) == len(other.word)}"
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, Word):
            return f"Are the words not equal? - {len(self.word) != len(other.word)}"
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, Word):
            return f"Is the first word longer than the second? - {len(self.word) > len(other.word)}"
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, Word):
            return f"Is the first word shorter than the second? - {len(self.word) < len(other.word)}"
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, Word):
            return f"Is the first word greater than or equal to the second? - {len(self.word) >= len(other.word)}"
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, Word):
            return f"Is the first word less than or equal to the second? - {len(self.word) <= len(other.word)}"
        return NotImplemented


# Example input and output:
word1 = Word(input("Enter a word: "))  # Example: "hello"
print(word1)  # Output: "Hello" (capitalized)
print(repr(word1))  # Output: "hello" (original representation)

# Input for the second word
word2 = Word(input("Enter a second word: "))  # Example: "world"

# Comparisons
print(word1 == word2)  # Output: Are the words equal? - True/False
print(word1 != word2)  # Output: Are the words not equal? - True/False
print(word1 > word2)   # Output: Is the first word longer than the second? - True/False
print(word1 < word2)   # Output: Is the first word shorter than the second? - True/False
print(word1 >= word2)  # Output: Is the first word greater than or equal to the second? - True/False
print(word1 <= word2)  # Output: Is the first word less than or equal to the second? - True/False
