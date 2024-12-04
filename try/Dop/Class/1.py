from math import *

class Aeroflot:
    def __init__ (self, name, number, type, timeh, timem):
        self.name = name
        self.number = number
        self.type = type
        self.timeh = timeh
        self.timem = timem
    def __str__(self):
        return f"Самолет под номером - {self.number}, типа - {self.type}, вылетает в город {self.name} в {self.timeh}:{self.timem}"
    def time (self, time_ph, time_pm):
        if time_ph * 60 + time_pm >= self.timeh * 60 + self.timem:
            return "Вы опоздали"
        else:
            return f"{abs(((self.timeh*60+self.timem) - (time_ph*60 +self.timem))// 60)}:{abs((self.timeh * 60 + self.timem) - (time_ph*60 + self.timem)) % 60}"
    
    
    def set_name (self, name):
        self.name = name
    def set_number (self, number):
        self.number = number
    def set_type (self, type):
        self.type = type
    def set_time (self, time):
        self.time = time
    def get_name (self, name):
        return self.name
    def get_number (self, number):
        return self, number
    def get_type (self, type):
        return self, type
    def get_time (self, time):
        return self.time
    
time_ph, time_pm = map(int, (input("Сколько осталось времени до вылета(h m): ").split()))
airplane = Aeroflot("Москва",123,"Пассажирский", 13, 30)
print(airplane)
print("До вылета осталось", airplane.time(time_ph, time_pm))