class Bachelor:
    def __init__(self, firstname, lastname, group, averageMark):
        self.firstname = firstname
        self.lastname = lastname
        self.group = group
        self.averageMark = averageMark
    def getScholarship(self):
        if self.averageMark == 5:
            return f"Scholorship of bachelor= 10000 rub"
        elif self.averageMark != 5 and self.averageMark >= 3:
            return f"Scholarship of bachelor= 5000 rub"
        else:
            return f"Scholarship of bachelor= 0 rub"
    def __str__(self):
        return f"Student - {self.firstname} {self.lastname}, from group №{self.group}"
class Undergraduate(Bachelor):
    def getScholarship(self):
        if self.averageMark == 5:
            return f"Scholorship of magistr = 15000 rub"
        elif self.averageMark != 5 and self.averageMark >= 3:
            return f"Scholorship of magistr = 7500 rub"
        else:
            return f"Scholarship of magistr = 0 rub"
ship1 = ["Semyon", "Ilin", 14123, 5] #scholorship == 10000 and 15000
ship2 = ["Aleksandr", "Shemetov", 14123, 3] #Scholorship == 5000 and 7500
ship3 = ["Egor", "Ship", 14121, 0] #Scholorship == 0 and 0
student = Bachelor(*ship1) 
student2 = Undergraduate(*ship3)
print(student.getScholarship())
print(student2.getScholarship())