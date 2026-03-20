# 15 Projects to Master Python Classes

A progressive set of projects that build your understanding of object-oriented programming in Python — from basic class structure to nuanced decisions about when to use instance methods, class methods, static methods, and properties.

Each project tells you **what to build**, **what to think about**, and **what to avoid** — but never gives you the solution.

> **Recommended reading before starting:**
> - [Python Docs — Classes](https://docs.python.org/3/tutorial/classes.html)
> - [Real Python — OOP in Python](https://realpython.com/python3-object-oriented-programming/)
> - [Real Python — Class vs Static vs Instance Methods](https://realpython.com/instance-class-and-static-methods-demystified/)

---

## Difficulty Scale

| Level | Focus |
|-------|-------|
| ⭐ Beginner | Defining classes, `__init__`, instance methods |
| ⭐⭐ Intermediate | Class variables, `@classmethod`, `@staticmethod` |
| ⭐⭐⭐ Advanced | `@property`, inheritance, method design decisions |

---

## Project 1 — Student Record ⭐

### What to build
A `Student` class that stores a student's name, age, and a list of grades. The class should be able to add a new grade, calculate the student's average grade, and return a summary string describing the student.

### Instructions

1. Define the class with an `__init__` method. Think carefully about what data belongs on each individual student — these become your instance variables.
2. Write a method to add a single grade to the student's grade list.
3. Write a method to compute and return the average of all grades. What should it return if no grades have been added yet?
4. Write a method that returns a human-readable string like: `"Alice, age 20, average grade: 85.4"`.
5. Create at least two student objects and call each method on them to verify they behave independently.

### What to think about
- Every method here uses `self` — ask yourself why. Could any of them work without it?
- What happens if you call the average method on a student with no grades? Handle that edge case gracefully.
- Why is the grade list created inside `__init__` rather than as a class variable?

### What NOT to do
- Do not use a class variable to store grades. Think about why this would break things if you had multiple students.

---

## Project 2 — Temperature Converter ⭐

### What to build
A `Temperature` class that stores a temperature value and its unit (Celsius, Fahrenheit, or Kelvin). The class should be able to convert between units and validate that a given temperature is physically possible.

### Instructions

1. Define `__init__` to accept a numeric value and a unit string.
2. Write three conversion methods: `to_celsius()`, `to_fahrenheit()`, and `to_kelvin()`. Each should return a new `Temperature` object in the target unit — not just a number.
3. Write a method `is_valid()` that returns `True` if the temperature is above absolute zero (−273.15°C).
4. Write a `@staticmethod` called `absolute_zero(unit)` that takes a unit string and returns the absolute zero value in that unit as a plain number.
5. Write a `__str__` method so that `print(temp)` outputs something like `"100°C"`.

### What to think about
- `is_valid()` uses `self` — it checks a specific instance's value. But `absolute_zero()` doesn't need any instance at all. What makes it a static method rather than a free function outside the class?
- Why does `absolute_zero` take a `unit` parameter if it's a static method?
- What is the difference between returning a new `Temperature` object vs returning a plain float from your conversion methods? Which is more useful and why?

### What NOT to do
- Do not put `absolute_zero` as an instance method. There is no reason it needs `self`.

---

## Project 3 — Bank Account ⭐

### What to build
A `BankAccount` class that models a simple bank account with deposit, withdrawal, and balance inquiry functionality.

### Instructions

1. Define `__init__` with an account holder's name and an optional starting balance (default to 0).
2. Write a `deposit(amount)` method that adds to the balance. It should reject non-positive amounts.
3. Write a `withdraw(amount)` method that subtracts from the balance. It should reject amounts greater than the current balance and non-positive amounts.
4. Write a `get_balance()` method that returns the current balance.
5. Add a class variable `interest_rate` set to `0.03` (3%). Write a method `apply_interest()` that multiplies the current balance by `1 + interest_rate`.
6. Write a `@classmethod` called `set_interest_rate(cls, rate)` that updates the class-level interest rate.

### What to think about
- `deposit`, `withdraw`, and `apply_interest` all use `self` — they operate on a specific account. But `set_interest_rate` uses `cls`. Why? Who "owns" the interest rate — one account or all accounts?
- What happens if you call `set_interest_rate` on an instance vs on the class directly? Try both.
- Why is it better to reject invalid deposits/withdrawals inside the method rather than expecting the caller to validate first?

### What NOT to do
- Do not use a global variable for `interest_rate`. The class variable is the right home for shared state.

---

## Project 4 — Book Library ⭐⭐

### What to build
A `Book` class and a `Library` class. The `Library` holds a collection of `Book` objects and supports searching, adding, and removing books.

### Instructions

1. `Book.__init__` should store title, author, year, and an `available` flag (default `True`).
2. Add a `@staticmethod` to `Book` called `is_valid_year(year)` that returns `True` if the year is a positive integer and not in the future.
3. `Library.__init__` should initialize an empty list of books.
4. Write `add_book(book)` on `Library` that adds a `Book` object. Use `Book.is_valid_year()` to validate before adding.
5. Write `find_by_author(author)` that returns a list of all books by that author.
6. Write `checkout(title)` that marks a book as unavailable, and `return_book(title)` that marks it available again.
7. Write a `@classmethod` on `Library` called `from_list(cls, book_data)` that takes a list of dictionaries (each with title, author, year) and returns a fully populated `Library` instance.

### What to think about
- `from_list` is an **alternative constructor** — a very common use case for `@classmethod`. Why can't `__init__` just handle this directly?
- `is_valid_year` is a `@staticmethod` on `Book`. Could it just be a free function at the module level? What do you gain by attaching it to the class?
- When `find_by_author` returns a list, should it return the actual `Book` objects or copies? What are the implications of each?

---

## Project 5 — Shape Calculator ⭐⭐

### What to build
A hierarchy of shape classes: a base `Shape` class, and subclasses `Circle`, `Rectangle`, and `Triangle`. Each shape can calculate its area and perimeter.

### Instructions

1. Define a base `Shape` class with a `color` attribute and a `describe()` method that prints the shape type and color.
2. Create `Circle(Shape)` with a `radius`. Add `area()` and `perimeter()` instance methods.
3. Create `Rectangle(Shape)` with `width` and `height`. Add `area()` and `perimeter()`.
4. Create `Triangle(Shape)` with three sides `a`, `b`, `c`. Add `area()` (use Heron's formula) and `perimeter()`.
5. Add a `@staticmethod` to `Shape` called `is_positive(*values)` that returns `True` if all given values are greater than zero. Use this inside each subclass's `__init__` to validate inputs.
6. Add a `@classmethod` to `Rectangle` called `square(cls, side, color)` that returns a `Rectangle` where width equals height.

### What to think about
- `square` is a `@classmethod` alternative constructor. What would be awkward about making it a regular `__init__` parameter like `Rectangle(side, side, color, is_square=True)`?
- `is_positive` is a `@staticmethod` on the base class. All subclasses can call `Shape.is_positive(...)`. Is this better than repeating the check in each subclass? Why?
- `area()` and `perimeter()` are instance methods — they depend on the specific dimensions of that shape. Could they ever be static or class methods? Why not?

---

## Project 6 — Employee Payroll System ⭐⭐

### What to build
An `Employee` class system with a base class and two subclasses: `HourlyEmployee` and `SalariedEmployee`. The system should calculate weekly pay correctly for each type.

### Instructions

1. `Employee.__init__` should store name and employee ID. Add a class variable `company_name`.
2. Add a `@classmethod` `set_company(cls, name)` to update the company name globally.
3. `HourlyEmployee` adds `hourly_rate` and `hours_worked`. Its `weekly_pay()` method multiplies the two. Hours above 40 should be paid at 1.5x the rate.
4. `SalariedEmployee` adds `annual_salary`. Its `weekly_pay()` divides annual salary by 52.
5. Add a `@staticmethod` to `Employee` called `format_currency(amount)` that returns a string like `"$1,234.56"`.
6. Add a `__str__` to each class that uses `format_currency` to display the employee's weekly pay.

### What to think about
- `weekly_pay()` is defined differently in each subclass — this is called **method overriding**. Each subclass has its own data (hours vs salary) that drives its own calculation.
- `format_currency` formats a number — it doesn't need any instance or class data. What would be wrong with making it an instance method just because it's "related" to employees?
- `company_name` is shared across all employees. What happens to existing instances when you call `set_company`? Test it.

---

## Project 7 — Inventory Tracker ⭐⭐

### What to build
A `Product` class and an `Inventory` class. The inventory tracks stock levels and generates low-stock alerts.

### Instructions

1. `Product.__init__` takes name, SKU (a unique identifier string), price, and quantity.
2. Add a `@property` called `total_value` that returns `price * quantity`. This should not be settable.
3. Add a `@staticmethod` to `Product` called `is_valid_sku(sku)` that returns `True` if the SKU is exactly 8 uppercase alphanumeric characters.
4. `Inventory` holds a list of `Product` objects. Write `add_product(product)` that validates the SKU before adding.
5. Write `low_stock_alert(threshold)` on `Inventory` that returns a list of products with quantity below the threshold.
6. Write a `@classmethod` on `Inventory` called `from_csv_rows(cls, rows)` where `rows` is a list of tuples `(name, sku, price, quantity)`. It should return a populated `Inventory`.
7. Write a `total_inventory_value()` method on `Inventory` that sums the `total_value` of all products.

### What to think about
- `total_value` is a `@property`. Why is it cleaner to write `product.total_value` than `product.get_total_value()`? What does the property communicate to another developer reading your code?
- Why should `total_value` not have a setter? What would go wrong if someone could write `product.total_value = 500`?
- `from_csv_rows` is an alternative constructor. How does using `cls(...)` inside a `@classmethod` instead of `Inventory(...)` directly make the code more inheritance-friendly?

---

## Project 8 — Playing Card Deck ⭐⭐

### What to build
A `Card` class and a `Deck` class. The deck can be shuffled, drawn from, and reset.

### Instructions

1. `Card.__init__` takes a `suit` (Hearts, Diamonds, Clubs, Spades) and a `rank` (2–10, Jack, Queen, King, Ace).
2. Add a `@staticmethod` to `Card` called `valid_suits()` that returns the list of valid suits, and `valid_ranks()` for valid ranks.
3. Add a `@property` to `Card` called `is_face_card` that returns `True` if the rank is Jack, Queen, or King.
4. `Deck.__init__` should build a full 52-card deck using the valid suits and ranks. Do not hardcode the cards — use `Card.valid_suits()` and `Card.valid_ranks()`.
5. Write `shuffle()` to randomize the deck in place (use the `random` module).
6. Write `draw()` to remove and return the top card. Handle an empty deck gracefully.
7. Write `reset()` to rebuild the deck to its full 52-card state.
8. Write a `@classmethod` called `two_decks(cls)` that returns a `Deck` containing 104 cards (two full decks combined).

### What to think about
- `valid_suits()` and `valid_ranks()` return data that belongs to the concept of a card — not to any specific card. Why are they static rather than instance methods?
- `is_face_card` is a `@property` on `Card`. It's computed from `self.rank`. Why is it better as a property than as a method `card.is_face_card()`?
- `two_decks` uses `cls()` internally. If you subclass `Deck` into `SpecialDeck`, what does `SpecialDeck.two_decks()` return? Try it.

---

## Project 9 — User Authentication System ⭐⭐

### What to build
A `User` class that models a user account with password hashing, login attempts, and account locking.

### Instructions

1. `User.__init__` takes a username and a plaintext password. Store the password as a hashed value — use Python's `hashlib.sha256`. Never store the plaintext password.
2. Add a class variable `max_attempts` set to `3`.
3. Add instance variables `failed_attempts` (starts at 0) and `locked` (starts at `False`).
4. Write a `login(password)` method that hashes the input and compares it to the stored hash. On failure, increment `failed_attempts`. Lock the account if `failed_attempts >= max_attempts`.
5. Write a `reset_attempts()` method that resets `failed_attempts` to 0 and unlocks the account.
6. Add a `@staticmethod` called `hash_password(password)` that takes a string and returns its SHA-256 hex digest. Use this inside `__init__` and `login`.
7. Add a `@classmethod` called `set_max_attempts(cls, n)` to change the lockout threshold globally.
8. Add a `@property` called `is_locked` that returns the `locked` flag.

### What to think about
- `hash_password` is a `@staticmethod`. It only takes a string and returns a string. No instance or class data needed. Why is it still useful to attach it to the `User` class rather than making it a module-level function?
- `is_locked` is a `@property`. What benefit does this give over just accessing `user.locked` directly? Think about what you could add later (logging, notifications) without changing calling code.
- `max_attempts` is a class variable. What happens if you change it on one instance — does it affect all users? Test this carefully.

---

## Project 10 — Vehicle Fleet Manager ⭐⭐⭐

### What to build
A `Vehicle` base class with subclasses `Car`, `Truck`, and `ElectricCar`. A `Fleet` class manages a collection of vehicles and generates reports.

### Instructions

1. `Vehicle.__init__` stores make, model, year, and mileage.
2. Add a `@property` `age` that computes the vehicle's age in years from the current year (import `datetime`).
3. Add a `@staticmethod` `is_valid_year(year)` that checks the year is between 1886 (the first car) and the current year.
4. `Car` adds `fuel_type`. `Truck` adds `payload_capacity`. `ElectricCar` adds `battery_range`.
5. Each subclass should override a `fuel_cost_per_mile(fuel_price)` method. For `Car`, use a fixed MPG of 30. For `Truck`, use 15 MPG. For `ElectricCar`, use `fuel_price` as cost per kWh and assume 4 miles per kWh.
6. `Fleet.__init__` starts with an empty list.
7. Add a `@classmethod` `from_dicts(cls, data)` that accepts a list of dicts and uses the `"type"` key to instantiate the correct subclass.
8. Write `cheapest_to_run(fuel_price)` on `Fleet` that returns the vehicle with the lowest `fuel_cost_per_mile`.
9. Add a `@property` `average_age` on `Fleet` that returns the mean age across all vehicles.

### What to think about
- `fuel_cost_per_mile` is overridden in each subclass with different logic. Each vehicle type has its own formula. How does Python know which version to call?
- `from_dicts` must decide which subclass to instantiate based on a string. How do you implement that dispatch logic cleanly? Think about using a dictionary mapping strings to classes.
- `average_age` is a `@property` on `Fleet` because it's a computed characteristic of the fleet — not a stored value. What would happen if you tried to assign to it?

---

## Project 11 — Recipe Cost Calculator ⭐⭐⭐

### What to build
An `Ingredient` class and a `Recipe` class. The system tracks ingredient costs and scales recipes up or down.

### Instructions

1. `Ingredient.__init__` takes name, unit (e.g., "grams"), quantity, and cost per unit.
2. Add a `@property` `total_cost` on `Ingredient` that returns `quantity * cost_per_unit`.
3. Add a `total_cost` setter that, when set, back-calculates and updates `cost_per_unit` accordingly.
4. `Recipe.__init__` takes a name and an empty list of ingredients.
5. Write `add_ingredient(ingredient)` to append an `Ingredient`.
6. Write a `@property` `total_cost` on `Recipe` that sums all ingredient costs.
7. Write `scale(factor)` that returns a **new** `Recipe` with all ingredient quantities multiplied by `factor`. The original recipe must remain unchanged.
8. Add a `@classmethod` `from_dict(cls, data)` where `data` is a dict with `"name"` and `"ingredients"` (a list of ingredient dicts).
9. Add a `@staticmethod` `convert_units(quantity, from_unit, to_unit)` that handles basic conversions (grams↔kg, ml↔L). Raise `ValueError` for unsupported conversions.

### What to think about
- The `total_cost` setter on `Ingredient` changes a stored attribute (`cost_per_unit`) based on a derived value. This is a valid use of a property setter — but what are the risks? When might this confuse someone reading the code?
- `scale` returns a new `Recipe` rather than modifying the original. Why is this often the right design decision? Think about immutability and unexpected side effects.
- `convert_units` has no need for instance or class data — it's pure math. But placing it on the `Recipe` class signals it belongs to the recipe domain. Is that good design or just clutter?

---

## Project 12 — Sports League Tracker ⭐⭐⭐

### What to build
A `Team` class and a `League` class that tracks match results and computes standings.

### Instructions

1. `Team.__init__` takes a team name. Initialize wins, losses, and draws all to 0.
2. Add a `@property` `points` that returns `wins * 3 + draws * 1`.
3. Add a `@property` `games_played` that returns `wins + losses + draws`.
4. Write a `record_result(outcome)` instance method where `outcome` is `"win"`, `"loss"`, or `"draw"`. Update the appropriate counter.
5. Add a `@staticmethod` `valid_outcome(outcome)` that returns `True` if the outcome is one of the three valid strings.
6. `League.__init__` takes a league name and an empty list of teams.
7. Write `add_team(team)` on `League`.
8. Write `record_match(team1_name, team2_name, result)` where `result` is `"home"` (team1 wins), `"away"` (team2 wins), or `"draw"`. Update both teams appropriately.
9. Write a `standings()` method that returns the list of teams sorted by points (descending), then by wins as a tiebreaker.
10. Add a `@classmethod` `new_season(cls, name, team_names)` that takes a league name and a list of team name strings, creates all the `Team` objects, and returns a ready-to-use `League`.

### What to think about
- `points` and `games_played` are `@property` methods because they are derived from stored data. If you stored them directly instead, what could go wrong when you update wins, losses, or draws?
- `new_season` is a `@classmethod` alternative constructor. What does using `cls(...)` inside it gain you over writing `League(...)` directly?
- `record_match` needs to look up teams by name. How do you find a team object from a string? Think about whether a list or a dict is the better internal data structure for the team collection.

---

## Project 13 — File Metadata Analyzer ⭐⭐⭐

### What to build
A `FileRecord` class that models metadata about a file (not the file itself) and a `FileCollection` class that groups and analyzes records.

### Instructions

1. `FileRecord.__init__` takes filename, size in bytes, and file extension.
2. Add a `@property` `size_kb` that returns size in kilobytes (rounded to 2 decimal places).
3. Add a `@property` `size_mb` that returns size in megabytes.
4. Add a `@staticmethod` `from_filename(filename, size)` that extracts the extension from the filename automatically (use `os.path.splitext`) and returns a `FileRecord`.
5. Add a `@staticmethod` `is_valid_extension(ext)` that returns `True` if the extension starts with `.` and contains only alphanumeric characters after it.
6. `FileCollection.__init__` starts with an empty list.
7. Write `add(record)` and `remove(filename)` methods.
8. Write a `@property` `total_size_mb` on `FileCollection` that sums sizes.
9. Write `by_extension()` that returns a dict mapping extension strings to lists of `FileRecord` objects.
10. Write a `largest(n)` method that returns the top `n` files by size.
11. Add a `@classmethod` `from_paths(cls, paths_and_sizes)` — a list of `(path, size)` tuples — using `FileRecord.from_filename()` internally.

### What to think about
- `from_filename` is a `@staticmethod` that acts as an alternative constructor for `FileRecord`. But it's `@staticmethod`, not `@classmethod`. What does that mean for subclassing? If you subclassed `FileRecord`, would `from_filename` return the right type?
- `size_kb` and `size_mb` are properties. Could you just store all three (bytes, KB, MB) in `__init__`? What problem does that create if size ever changes?
- `by_extension` returns a dict. Should the lists in that dict contain the original objects or copies? What are the tradeoffs?

---

## Project 14 — Subscription Billing Engine ⭐⭐⭐

### What to build
A subscription billing system with a `Plan` class, a `Subscriber` class, and a `BillingEngine` class.

### Instructions

1. `Plan.__init__` takes a name, monthly price, and a list of features.
2. Add a `@classmethod` for each of three preset plans: `Plan.basic()`, `Plan.standard()`, `Plan.premium()`. Each returns a `Plan` with hardcoded values appropriate for that tier.
3. Add a `@property` `annual_price` that returns `monthly_price * 12`.
4. Add a `@staticmethod` `compare(plan_a, plan_b)` that returns the plan with more features.
5. `Subscriber.__init__` takes a name, email, and a `Plan` object. Add a `joined_date` using `datetime.date.today()`.
6. Add a `@property` `months_subscribed` that computes how many full months since `joined_date`.
7. Add a `upgrade(new_plan)` instance method that replaces the current plan. Track the old plan in an `upgrade_history` list.
8. `BillingEngine.__init__` holds a list of subscribers and a billing month.
9. Write `run_billing()` that returns a list of `(subscriber_name, amount_due)` tuples for all subscribers.
10. Write `revenue_by_plan()` that returns a dict of `plan_name → total_revenue` for the current billing cycle.

### What to think about
- `Plan.basic()`, `Plan.standard()`, `Plan.premium()` are all `@classmethod` alternative constructors. Why is this cleaner than passing a `tier` string to `__init__` and switching inside it?
- `annual_price` is a `@property`. If `monthly_price` could change (e.g., on promotion), what happens to `annual_price`? Is it always accurate? This is the key advantage of computing it on the fly.
- `compare` is a `@staticmethod` — it takes two `Plan` objects as arguments and returns one. Why not make it an instance method like `plan_a.compare_to(plan_b)`? Is one style more readable?

---

## Project 15 — Text Adventure Game Engine ⭐⭐⭐

### What to build
A small engine for a text adventure game with `Room`, `Item`, `Player`, and `Game` classes.

### Instructions

1. `Room.__init__` takes a name, description, and an empty dict of exits (`{"north": room_object, ...}`).
2. `Item.__init__` takes a name, description, and weight. Add a `@staticmethod` `is_valid_weight(weight)` that returns `True` for positive numbers.
3. `Player.__init__` takes a name and a starting `Room`. Initialize an empty inventory list and a health value of 100.
4. Add a `@property` `carry_weight` on `Player` that returns the total weight of all inventory items.
5. Add a `@property` `is_alive` that returns `True` if health > 0.
6. Write `pick_up(item)` that adds to inventory, and `drop(item)` that removes it. Neither should allow carrying more than a max weight — use a class variable `MAX_CARRY = 50`.
7. Write `move(direction)` that changes the player's current room if the exit exists; otherwise prints a message.
8. `Game.__init__` takes a player and a list of rooms. Track a `turn_count` class variable (shared across all game instances — think about whether this is the right design).
9. Write a `@classmethod` `new_game(cls, player_name)` that builds a small pre-configured world of at least 3 connected rooms and returns a ready-to-play `Game`.
10. Write `take_turn(action)` that parses simple string commands like `"go north"`, `"pick up sword"`, `"drop torch"`.

### What to think about
- `turn_count` as a class variable on `Game` means all game instances share the same counter. Is this the right behavior? When would you want a class variable here vs an instance variable? Deliberately decide, and write a comment explaining your choice.
- `carry_weight` and `is_alive` are properties. Both could have been stored attributes — but why does computing them on the fly make the code more reliable?
- `new_game` builds an entire world and returns a `Game`. How does the `@classmethod` pattern make this cleaner than a separate factory function at the module level?
- Look back at all 15 projects. Which ones forced you to reach for `@classmethod`? When was `@staticmethod` the right call? When did `@property` make code cleaner? Reflect on the pattern.

---

## Summary: What Each Project Exercises

| Project | Instance Method | Class Method | Static Method | Property |
|---------|:-:|:-:|:-:|:-:|
| 1. Student Record | ✅ | | | |
| 2. Temperature | ✅ | | ✅ | |
| 3. Bank Account | ✅ | ✅ | | |
| 4. Book Library | ✅ | ✅ | ✅ | |
| 5. Shape Calculator | ✅ | ✅ | ✅ | |
| 6. Employee Payroll | ✅ | ✅ | ✅ | |
| 7. Inventory Tracker | ✅ | ✅ | ✅ | ✅ |
| 8. Card Deck | ✅ | ✅ | ✅ | ✅ |
| 9. User Auth | ✅ | ✅ | ✅ | ✅ |
| 10. Fleet Manager | ✅ | ✅ | ✅ | ✅ |
| 11. Recipe Cost | ✅ | ✅ | ✅ | ✅ |
| 12. League Tracker | ✅ | ✅ | ✅ | ✅ |
| 13. File Analyzer | ✅ | ✅ | ✅ | ✅ |
| 14. Billing Engine | ✅ | ✅ | ✅ | ✅ |
| 15. Text Adventure | ✅ | ✅ | ✅ | ✅ |

---

## Further Reading

- [Python Docs — `@property`](https://docs.python.org/3/library/functions.html#property)
- [Real Python — Python's `super()` Considered Super](https://realpython.com/python-super/)
- [Real Python — Inheritance and Composition](https://realpython.com/inheritance-composition-python/)
- [Python Docs — Data Model (`__str__`, `__repr__`, etc.)](https://docs.python.org/3/reference/datamodel.html)
