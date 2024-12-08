classes = int(input("Enter the number of classes: "))
boys = int(input("Enter the total number of boys: "))
girls = int(input("Enter the total number of girls: "))

classes_data = {}

boys_per_class = boys // classes
extra_boys = boys % classes
girls_per_class = girls // classes
extra_girls = girls % classes

for i in range(1, classes + 1):
    num_boys = boys_per_class + (1 if i <= extra_boys else 0)
    num_girls = girls_per_class + (1 if i <= extra_girls else 0)
    classes_data[i] = (num_boys, num_girls)

sorted_classes = sorted(classes_data.items(), key=lambda x: x[1][0] / (x[1][0] + x[1][1]))

print("\nClasses sorted by increasing percentage of boys:")
for cls, (num_boys, num_girls) in sorted_classes:
    percent_boys = (num_boys / (num_boys + num_girls)) * 100
    print(f"Class {cls}: {percent_boys:.2f}% boys")

more_boys = [cls for cls, (num_boys, num_girls) in classes_data.items() if num_boys > num_girls]

print("\nClasses with more boys than girls:")
if more_boys:
    print(", ".join(map(str, more_boys)))
else:
    print("No classes with more boys than girls.")


#exampleEnter the number of classes: 3
#Enter the total number of boys: 10
#Enter the total number of girls: 8
#Enter the number of classes: 3
#Enter the total number of boys: 10
#Enter the total number of girls: 8
