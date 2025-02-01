file = open("text.txt", "w")
file.write("Hello world \n"
           "Kak dela privet")

file = open("text.txt", "r", encoding="utf-8")    
print(file.read())
print(file.readlines())
file.close()
