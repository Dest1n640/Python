class Bilet:
    def __init__(self, number, price, place, timeh, timem, data, IsVirtual):
        self.number = number
        if price > 0:
            self.price = price
        else:
            raise ValueError("Price must be positive.")
        self.place = place
        self.timeh = timeh
        self.timem = timem
        self.data = data
        self.IsVirtual = IsVirtual

        if IsVirtual == 1:
            print("Билет отправлен на email")
        else:
            print("Вот ваш билет:")

    def __str__(self):
        return (f"Номер билета - {self.number}, цена за билет - {self.price}, "
                f"место билета - {self.place}, время - {self.timeh}:{self.timem}, дата - {self.data}")

    def sell(self):
        return f"Билет продан за {self.price}"

    def pas(self):
        return f"Билет сдан за {self.price // 2}"

    def anul(self):
        return "Билет аннулирован"

class Transport(Bilet):
    def __init__(self, number, price, place, timeh, timem, data, IsVirtual, train=None, airplane=None):
        self.train = train
        self.airplane = airplane

class Train(Transport):
    def __init__(self, number, price, place, timeh, timem, data, IsVirtual, type_class):
        self.type_class = type_class

    def __str__(self):
        return f"Класс на поезде - {self.type_class}"

class Airplane(Transport):
    def __init__(self, number, price, place, timeh, timem, data, IsVirtual, type_class):
        self.type_class = type_class

    def __str__(self):
        return f"Класс на самолете - {self.type_class}"

class Event(Bilet):
    def __init__(self, number, price, place, timeh, timem, data, IsVirtual, name):
        self.name = name

    def __str__(self):
        return f"Название мероприятия - {self.name}"

# Create an instance of Bilet
user1 = Bilet(123, 5000, 1, 12, 30, "24.12.2024", 1)
print(user1)
