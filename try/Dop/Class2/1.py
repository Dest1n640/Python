# Есть основной класс билет, (Может быть на концерт, на автобус и т.д.)
# Номер, цена, место, время, дата                (isVirtual)
# Купить(), Сдать, Продать, Аннулировать
# Транспортные(от, до), Мероприятие(Название мероприятия)
# Транспортные - жд, авио,
#ЖД - св, купе, плацкарт
# Авио - эконом, ср, бизнес 

class Bilet:
    def __init__(self, number, price, place, timeh, timem, data, IsVirtual):
        self.number = number
        if price > 0:
            self.price = price
        else:
            raise ValueError()
        self.place = place
        self.timeh = timeh
        self.timem = timem
        self.data = data
        self.IsVirtual = IsVirtual
        if IsVirtual == 1:
            return f"Билет отправлен на email"
        else:
            return f"Вот ваш билет: "
        
    def __str__(self):
        return f"Номер билета - {self.number}, цена за билет - {self.price}, место билета - {self.place}, время - {self.timeh}:{self.timem} дата - {self.data}"
    def sell (self):
        return f"Билет проданн за {self.price}"
    def pas (self):
        return f"Билет сдан за {self.price//2}"
    def anul (self):
        return f"Билет анулирован"
class Transport(Bilet):
    def __init__(self, train, airplane):
        self.train = train
        self.airplane = airplane
class Train(Transport):
    def __init__(self, sv, kupe, plazcart):
        if self.price == 3000:
            self.sv = sv
            type = sv
        elif self.price == 5000:
            self.plazcart = plazcart
            type = self.plazcart
        elif self.price == 10000:
            self.kupe = kupe
            type = plazcart
    def __str__(self, type):
        return f"Класс на поезде - {type}"
    
class Airplane(Transport):
    def __init__(self, eco, mid, bus):
        if self.price == 5000:
            self.eco = eco
            type = self.eco
        elif self.price == 10000:
            self.mid = mid
            type = self.mid
        else:
            self.bus = bus
            type = bus
    def __str__ (self, type):
        return f"Класс на самолете - {type}"
class Event(Bilet):
    def __init__(self,name):
        self.name = name
    def __str__(self):
        return f"Название меропрития {self.name}"

user1 = Bilet(123, 5000, 1,12, 30, 24, 1)
print(user1)    