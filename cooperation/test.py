from abc import ABC

class ab(ABC):
    def __init__(self,val):
        self.val=val
    def function(self, a):
        print(a+self.val)

class child(ab):
    def __init__(self, val):
        super().__init__(val)
    def function(self, a):
        super().function(a)
        print(self.val*a)

if __name__=="__main__":
    c = child(5)
    c.function(3)
