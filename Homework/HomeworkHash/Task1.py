def rabin_karp(text, pattern):
    n = len(text)
    m = len(pattern)
    
    base = 256
    q = 101
    
    pattern_hash = 0
    window_hash = 0
    h_base = 1
    
    for i in range(m - 1):
        h_base = (h_base * base) % q
    
    for i in range(m):
        pattern_hash = (pattern_hash * base + ord(pattern[i])) % q
        window_hash = (window_hash * base + ord(text[i])) % q
    
    matches = []
    for i in range(n - m + 1):
        if pattern_hash == window_hash:
            if text[i:i + m] == pattern:
                matches.append(i)
        
        if i < n - m:
            window_hash = (window_hash - ord(text[i]) * h_base) * base + ord(text[i + m])
            window_hash %= q
            if window_hash < 0:
                window_hash += q
    
    return matches

text = "Hello Hello Hello"
pattern = "llo"

result = rabin_karp(text, pattern)
print(result)
