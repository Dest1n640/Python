def number29(haystack, needle):
    m = len(haystack)
    n = len(needle)
    for i in range(m - n + 1):
        if haystack[i : i + n] == needle:
            return 0
        else:
            return -1


haystack = "sadbutsad"
needle = "sad"
print(number29(haystack, needle))
