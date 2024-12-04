# class Names:
#     def __init__(self, name_str = "Сергей", num_slog = 2):
#          self.name = name_str
#          self.num_sl = num_slog
#          self.length = len(self.name)
    
#     def __str__(self):
#          return self.name + " " + "Ударение на слог" + str(self.num_sl)
         
#     def count_letter(self):
#         list_let = ["а", "о", "у", "ы", "э", "ю", "я", "и", "е", "ё"]
#         count = 0
#         for letter in self.name.lower():
#             if letter in list_let:
#                 count+=1
#         return count
    
    
# name1 = Names("Александр", 2)
# name2 = Names("Alejandro", 3)

# print(name1.name)
# print(name1.num_sl)
# print(name1.length) 
# print(name2.length)
# print (name1.count_letter())



class Ndrob:
    def __init__(self, numinator = 1, denominator = 1):
        self.num = numinator
        if denominator != 0:
            self.denom = denominator
        else:
            print("Error")
            self.denom = None
            
    def __str__(self):
        return str(self.num) + "/" + str(self.denom)
    
    
    def multy_frac(self, other_frank):
        res = Ndrob()
        res.num = self.num * other_frank.num
        res.denom = self.denom * other_frank.denom
        return res      
    
frank1 = Ndrob(3,4)
frank2 = Ndrob(5,7)
frank3 = frank1.multy_frac(frank2)
print(frank3)     

        

    
# name1 = Names(), For
# #name1.length = 12 #Нельзя так делать кароче 
# name2 = Names()
# print(name2.length)
# print(name1.length)
# print(name2.length)
# Names.length = 30
# print(name2.length)
# print(name1.length)