def are_one_char_diff(str1, str2):
    if str1 == str2: 
        return False
    
    if len(str1) != len(str2):
        return False
    
    count_diff = 0

    for i in range(len(str1)):
        if str1[i] != str2[i]:
            count_diff += 1
            if count_diff > 1: 
                return False
            
    return count_diff == 1

def count_suspect_words(gods, suspects):
    result = []
    
    for god in gods:
        count = 0
        for suspect in suspects:
            if are_one_char_diff(god, suspect): 
                count += 1
        result.append(count) 

    return result


N = int(input("Enter number of gods' names: "))
gods = [input().strip() for _ in range(N)] 
M = int(input("Enter number of suspect names: "))
suspects = [input().strip() for _ in range(M)]

results = count_suspect_words(gods, suspects)
print(" ".join(map(str, results)))
