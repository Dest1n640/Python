from email.policy import strict


class Father:
    def __init__(self, mood = "neutral"):
        self.mood = mood
    def greet(self):
        return "Hello!"
    def be_strict(self):
        self.mood = "strict"
        return self.mood

class Mother:
    def __init__(self, mood = "neutral"):
        self.mood = mood
    def greet(self):
        return "Hi, honey!"
    def be_kind(self):
        self.mood = "kind"
        return self.mood

class Daughter(Father, Mother):
    def __init__(self, mood = "neutral"):
        Mother.__init__(self, mood)

class Son(Father, Mother):
    def __init__(self, mood="neutral"):
        Father.__init__(self,mood)

f = Father()
f.be_strict()
m = Mother()
m.be_kind()
d = Daughter()
d.be_strict()
s = Son()
s.be_kind()
for i in (f, m, d, s):
    print(f"{i.__class__.__name__}: {i.greet()}, mood: {i.mood}")