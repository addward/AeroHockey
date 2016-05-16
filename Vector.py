import math

class Vector:
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def __add__(self, b):
        new = Vector(self.x, self.y)
        new.x = self.x + b.x
        new.y = self.y + b.y
        return new

    def __sub__(self, b):
        new = Vector(self.x, self.y)
        new.x = self.x - b.x
        new.y = self.y - b.y
        return new

    def __mul__(self, b):
        if (type(b) is Vector):
            res = self.x * b.x + self.y * b.y
            return res
        elif (type(b) is float or type(b) is int):
            new = Vector(self.x, self.y)
            new.x = b * new.x
            new.y = b * new.y
            return new
        else:
            print ("Error")
            return 'Error'

    def mod(self):
        mod=self.x**2 + self.y**2
        return math.sqrt(mod)