'''
Alright, here's your assignment.
I need you to build out our employee payroll system. We have two types of employees — 
hourly and salaried. They get paid differently, so the system needs to handle both.

Build me an Employee base class. Every employee has a name, an ID, and they all work 
for the same company. Then build out HourlyEmployee and SalariedEmployee as subclasses. 
Each one calculates weekly pay its own way.

For hourly workers, keep in mind that anything over 40 hours is overtime and gets paid 
at time and a half. 
Salaried workers get the same check every week based on their annual salary.

I also want a clean way to display money — no one wants to see 1234.5, they want to see $1,234.56.
Build that as a utility and make sure it shows up when you print any employee.
One more thing — if we ever rebrand or get acquired, I need to be able to change the company
 name once and have it update everywhere. Every employee, past and present, should reflect the new name.
Send me what you've got when you're done and we'll review it together.
'''

class Employee:
    company = "Pepsi"
    def __init__(self, name, id):
        self.name = name
        self.id = id
    @classmethod
    def company_name(cls,company_name):
        cls.company = company_name
    @staticmethod
    def money_format(money):
        if not isinstance(money, (int,float)):
            raise ValueError ("Needs to be int")
        m = (f"${money:,.2f}")
        return m
    
'''
#To call a variable from another class or another: Employee.money_format(self.weekly_check())
'''       
class Salaried(Employee):
    def __init__(self,annual_salary,name, id):
        super().__init__(name, id)
        self.annual_salary = annual_salary
    def weekly_check(self):
        pay_check = (self.annual_salary / 52) * 2
        return pay_check
    def __str__(self):
        return f'Name {self.name}, ID {self.id}, Money {Employee.money_format(self.weekly_check())}' 
    
'''
#In def __str__(self): You don't use print you use return. 
'''
class Hourly(Employee):
    def __init__(self, pay, hours,name, id):
        super().__init__(name, id)
        self.pay = pay
        self.hours = hours
    def bi_weekly_pay(self):
        if self.hours > 40:
            ot = self.hours - 40
            pay_check = (self.pay * (self.hours - ot)) * 2 + (self.pay * ot * 1.5)
        else:
            pay_check = (self.pay * self.hours) * 2
        return pay_check
    def __str__(self):
        return f'Name {self.name}, ID {self.id}, Money {Employee.money_format(self.bi_weekly_pay())}' 
    

    
