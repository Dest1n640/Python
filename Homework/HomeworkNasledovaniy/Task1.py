class Counter:
    def __init__(self, start=0):
        self.value = max(0, start)

    def inc(self, amount=1):
        self.value += amount
        return self.value

    def dec(self, amount=1):
        self.value = max(0, self.value - amount)
        return self.value
    def __str__(self):
        return f"Value = {self.value}"
class NonDecCounter(Counter):
    def dec(self, amount=1):
        pass
class LimitedCounter(Counter):
    def __init__(self, start = 0, limit = 10):
        Counter().__init__(start)
        self.value = max (0, start)
        self.limit = limit
          
    def inc(self, number):
        if self.value + number > self.limit:
            raise ValueError("Sum of value and number bigger then limit")
        else:
            self.value += number
            return self.value
# Example for Counter
counter = Counter(5)
print(counter) #output 5
print(counter.inc(5)) #output 10
print(counter.dec(7)) #output 3

#Example for NonDecCounter
non_dec_counter = NonDecCounter(7)
print(non_dec_counter) #output 7
print(non_dec_counter.inc(5)) #output 12
print(non_dec_counter.dec(10)) #output None

#Example for LimitedCounter
limited_counter =  LimitedCounter(5)
print(limited_counter) #output 5
print(limited_counter.inc(5)) #output 10
print(limited_counter.dec(7)) #output 3
# also for error
# print(limited_counter.inc(20))