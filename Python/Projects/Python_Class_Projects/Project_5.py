import math as math

class Shape:
    def __init__(self, color):
        self.color = color
    def describe(self):
        print(f'Shape color {self.color}')
    @staticmethod
    def is_positive(*values):
        for v in values:
            if v <= 0:
                return False
        #Point of confusion
        return True

class Circle(Shape):
    def __init__(self, color, radius):
        #Point of confusion: The logic here and raise ValueError
        if not Shape.is_positive(radius):
            raise ValueError("Radius must be positive")
        #Point of confusion: super(). is something i need to review
        super().__init__(color)
        self.radius = radius
    def area(self):
        a = math.pi * self.radius**2
        return a
    def perimeter(self):
        p = 2 * math.pi * self.radius
        return p
    def describe(self):
        print(f'Circle color: {self.color}')
    

class Rectangle(Shape):
    def __init__(self, color, width, height):
        if not Shape.is_positive(width,height):
            raise ValueError ("Must be positive integer")
        super().__init__(color)
        self.width = width 
        self.height = height 
    def area(self):
        a2 = self.width * self.height 
        return a2 
    def perimeter(self):
        p2 = 2 * (self.height + self.width)
        return p2
    def describe(self):
        print(f'Rectangle color: {self.color}')
    
    @classmethod 
    def square(cls, side, color):
        new_square = cls(color, side, side)
        return new_square
        



class Triangle(Shape):
    def __init__(self, color, a, b, c):
        if not Shape.is_positive(a,b,c):
            raise ValueError("Must be positive")
        super().__init__(color)
        self.a = a
        self.b = b
        self.c = c
    def area(self):
        a3 = (self.a + self.b + self.c)/2
        return a3
    def perimeter(self):
        p3 = self.a + self.b + self.c
        return p3
    def describe(self):
        print(f'Triangle color: {self.color}')

    
    
        




#class Circle:
#class Rectangle:
#class Triangle: