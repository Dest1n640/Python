def longestCommonPrefix(strs):
    if not strs:
        return ""

    prefix = ""
    for i in range(len(strs[0])):
        char = strs[0][i]
        for string in strs[1:]:
            if i >= len(string) or string[i] != char:
                return prefix
        prefix += char
    return prefix

strs = [str(i) for i in input("Input elements: ").split()]

print(longestCommonPrefix(strs))
