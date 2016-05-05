import math

class Vector:
    def __init__(self,a):
        self.koord = a
        self.len = len(a)
    def __add__(self, b):
        if (self.len == b.len):
            new = Vector(list(self.koord))
            for i in range(b.len):
                new.koord[i] = self.koord[i]+b.koord[i]
            return new
        else:
            print ("Error")
            Vector.koord="Error"
            return Vector
    def __sub__(self, b):
        if (self.len == b.len):
            new = Vector(list(self.koord))
            for i in range(b.len):
                new.koord[i] = self.koord[i] - b.koord[i]
            return new
        else:
            print ("Error")
            Vector.koord="Error"
            return Vector
    def __mul__(self, b):
        if (type(b) is Vector):
            if (self.len==b.len):
                res=0
                for i in range(b.len):
                    res+=self.koord[i]*b.koord[i]
                return res
        elif (type(b) is float or type(b) is int):
            new = Vector(list(self.koord))
            for i in range(self.len):
                    new.koord[i]=b*new.koord[i]
            return new
        else:
            print ("Error")
            return 'Error'
    def mod(self):
        mod=0
        for i in range(self.len):
            mod+=self.koord[i]**2
        return math.sqrt(mod)