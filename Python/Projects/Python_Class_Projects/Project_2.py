'''
## Project 2 — Temperature Converter ⭐

### What to build
A `Temperature` class that stores a temperature value and its unit (Celsius, Fahrenheit, or Kelvin). 
The class should be able to convert between units and validate that a given temperature is 
physically possible.

### Instructions

1. Define `__init__` to accept a numeric value and a unit string.
2. Write three conversion methods: `to_celsius()`, `to_fahrenheit()`, and `to_kelvin()`. 
Each should return a new `Temperature` object in the target unit — not just a number.
3. Write a method `is_valid()` that returns `True` if the temperature is above absolute zero 
(−273.15°C).
4. Write a `@staticmethod` called `absolute_zero(unit)` that takes a unit string and 
returns the absolute zero value in that unit as a plain number.
5. Write a `__str__` method so that `print(temp)` outputs something like `"100°C"`.
'''
class Temp_Converter:
    def __init__(self, temp,unit):
        self.temp = temp
        self.unit = unit
    def __str__(self):
        return f'{self.temp}{self.unit}'
    
    def to_celsius(self):
        if self.unit == "C":
            return Temp_Converter(self.temp,self.unit)
        elif self.unit == "F":
            converted_c = (self.temp - 32) * (5/9)
            return Temp_Converter(converted_c, 'C')
        elif self.unit == "K":
            converted_c2 = self.temp - 273.15
            return Temp_Converter(converted_c2, 'C')


    def to_fahrenheit(self):
        if self.unit == "F":
            return Temp_Converter(self.temp,self.unit)
        elif self.unit == "C":
            convertedt = (self.temp*9/5) + 32
            return Temp_Converter(convertedt, 'F')
        elif self.unit == "K":
            celsius = self.temp - 273.15
            converted_t2 = (celsius * 9/5) + 32
            return Temp_Converter(converted_t2, 'F')

    def to_kelvin(self):
        if self.unit == 'K':
            return Temp_Converter(self.temp,self.unit)
        elif self.unit == 'F':
            convert_k = (self.temp - 32) * (5/9) + 273.15
            return Temp_Converter(convert_k, 'K')
        elif self.unit == 'C':
            convert_k2 = self.temp + 273.15
            return Temp_Converter(convert_k2, 'K')
    
    def is_valid(self):
        return self.to_celsius().temp > -273.15 
    
    @staticmethod
    def absolute_zero(unit):
        if unit == 'K':
            return 0
        elif unit == 'C':
            return -273.15
        elif unit == 'F':
            return -459.67
    
    def __str__(self):
        return f'{self.temp}°{self.unit}'
    
temp1 = Temp_Converter(85, "F")
print(temp1.to_celsius())
print(temp1.is_valid())
    
'''
### What to think about
- `is_valid()` uses `self` — it checks a specific instance's value. But `absolute_zero()` 
doesn't need any instance at all. What makes it a static method rather than a free function 
outside the class?
- Why does `absolute_zero` take a `unit` parameter if it's a static method?
- What is the difference between returning a new `Temperature` object vs returning a plain float 
from your conversion methods? Which is more useful and why?

### What NOT to do
- Do not put `absolute_zero` as an instance method. There is no reason it needs `self`.
'''