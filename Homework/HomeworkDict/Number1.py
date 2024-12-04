classes = int(input("Введите сколько всего классов: "))
boys = int(input('Введите количество мальчиков в классах: '))
girls = int(input('Введите количество девочек в классах: '))

my_dict_boys = {}
my_dict_gils = {}

boys_per_class = boys // classes
extra_boys = boys % classes
girl_pre_class = girls // classes
extra_girls = girls % classes

for i in range(1, classes + 1):
    if i <= extra_boys:
        my_dict_boys[i] = boys_per_class+1
    else:
        my_dict_boys[i] = boys_per_class
        
for i in range(1, classes + 1):
    if i <= extra_girls:
        my_dict_gils[i] = girl_pre_class+1
    else:
        my_dict_gils[i] = girl_pre_class
        

for key1, value1 in my_dict_boys.items():
    print (f"Class {key1} boys {value1}")
        
for key2, value2 in my_dict_gils.items():
    if value1 < value2:
        print(f"Class {key2} where boys < than girls")
    
#examples classes = 10, boys = 155, girls = 160 then
# Class 1 boys 16
# Class 2 boys 16
# Class 3 boys 16
# Class 4 boys 16
# Class 5 boys 16
# Class 6 boys 15
# Class 7 boys 15
# Class 8 boys 15
# Class 9 boys 15
# Class 10 boys 15
# Class 1 where boys < than girls
# Class 2 where boys < than girls
# Class 3 where boys < than girls
# Class 4 where boys < than girls
# Class 5 where boys < than girls
# Class 6 where boys < than girls
# Class 7 where boys < than girls
# Class 8 where boys < than girls
# Class 9 where boys < than girls
# Class 10 where boys < than girls    correct
    
        

