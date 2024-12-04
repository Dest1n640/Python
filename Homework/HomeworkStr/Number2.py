my_str = str(input())
count = 0
for ind, i in enumerate(my_str):
    if my_str[ind-2].isupper() == True and my_str[ind-1].islower() == True and my_str[ind].islower() == False:
        count+=1
    elif my_str[ind-3].isupper() == True and my_str[ind-2].islower() == True and my_str[ind-1].islower() == True and my_str[ind].islower() == False:
        count+=1
    elif my_str[ind-4].isupper() == True and my_str[ind-3].islower() == True and my_str[ind-2].islower() == True and my_str[ind-1].islower() == True and my_str[ind].islower() == False:
        count += 1       #count words which correct
    
def letters(upper_letter): 
    for i in my_str:
        if i.isupper():
            upper_letter += 1  #count number words with upper letter
    return (upper_letter)
            
if count == letters(0):
    print(True)
else:
    print(False)
# IoIsTheBest  4 words, all correct >>> True
# IoItIsWaste  4 words, Waste incorrect >>>False