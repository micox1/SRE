'''
## Project 3 — Bank Account ⭐

### What to build
A `BankAccount` class that models a simple bank account with deposit, withdrawal, and balance inquiry functionality.

### Instructions

1. Define `__init__` with an account holder's name and an optional starting balance (default to 0).
2. Write a `deposit(amount)` method that adds to the balance. It should reject non-positive amounts.
3. Write a `withdraw(amount)` method that subtracts from the balance. 
It should reject amounts greater than the current balance and non-positive amounts.
4. Write a `get_balance()` method that returns the current balance.
5. Add a class variable `interest_rate` set to `0.03` (3%). Write a method `apply_interest()` 
that multiplies the current balance by `1 + interest_rate`.
6. Write a `@classmethod` called `set_interest_rate(cls, rate)` that updates the class-level 
interest rate.
'''
class BankAccount:
    interest_rate= 0.03
    def __init__(self, name, balance = 0):
        self.name = name
        self.balance = balance 
    
    def deposit(self, amount):
        if amount <= 0:
            return f"Unable to deposit ${amount}"
        self.balance += amount    # this changes the actual balance
        return self.balance
    
    def withdraw(self, amount):
        if amount <= 0:
            return f'Unable to withdraw ${amount}'
        elif amount > self.balance:
            return f'Unable to withdraw ${amount}'   
        else:
            self.balance -= amount
            return self.balance
            
    def get_balance(self):
        return self.balance
    
    
    def apply_interest(self):
        self.balance = self.balance * (1 + self.interest_rate)
    
    @classmethod
    def set_interest_rate(cls, rate):
        cls.interest_rate = rate
         
'''
### What to think about
- `deposit`, `withdraw`, and `apply_interest` all use `self` — they operate on a specific account. But `set_interest_rate` uses `cls`. Why? Who "owns" the interest rate — one account or all accounts?
- What happens if you call `set_interest_rate` on an instance vs on the class directly? Try both.
- Why is it better to reject invalid deposits/withdrawals inside the method rather than expecting the caller to validate first?

### What NOT to do
- Do not use a global variable for `interest_rate`. The class variable is the right home for shared state.

---
'''

