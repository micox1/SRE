# Variables 
- Variables are assigned using `=`

Example:
```python 
message_string = "Hello There"
print(message_string)

#This would print the contents of the message_string which would be "Hello There"
```

# Numbers 
- int is a whole number 
- float is a decimal number 
- ** is used for exponents

## Modulo Operator 
- The modulo operator is indicated by `%` and gives the remainder of a division calculation. If two numbers are divisible then the result of the modulo operation will be `0`
```python 
print(29 % 5) #Prints 4 because it is the remainder 
print(3 % 3) #Prints 0 
print(7 % 3) #Prints 1
```

## Concatenation 
- The `+` operator doesn't just add two numbers it can also add two strings 
- To concatenate a string with a number you need to use str() first

## Plus Equal
- When you have a number saved in a variable and you want to add the current value of the variable you can use `+=`
- You can use the `+=` for string as well

# Boolean Expressions
- A boolean expression is a statement that can either be true or false. 
- The statement must be answered by true or false only and it must be verifiable with evidence 

## Relational Operators 
- We create boolean expressions using relational and logical operators
- Relational Operators compare two values and return True or False based on the operands 
    - `==` returns True if both its operands are the same otherwise it is False
    - `!=` is the not equals sign
    - `>` is greater than 
    - `>=` is greater than or equal to
    - `<` less than 
    - `<=` less than or equal to 
- Logical Operators are used to combine multiple Boolean expressions
    - You can make a variable set to True or False to make them boolean
## Boolean Operators 
- These operators combine smaller boolean expressions into larger boolean expressions 
    - The following are boolean operators 
        - `and` combines two boolean expressions and evaluates if both are True or False 
        -`or` one of the other will be either True or False 
        -`not` when applied to any boolean expression it reverses the boolean value
Examples:
```python
if (credits >= 120) and (gpa >= 2.0):
    print("Congrats you passed!")
```

## If Statements 

Example 
```python
if is_raining:
    print("bring an Umbrells")
```
- The colon `:` tells the computer that what is coming next is what shoyld be executed if the condition is met

### Else if (elif) Statements 
- An elif statement checks another condition after the previous `if` statement's conditions aren't met 
- We can use `elif` to control the order we want our program to check each of our conditional statements 
    - Firs the if statement is checked than the elif statement than the else 

## Match Statements 
- We can also use switch statements to build a program's flow control 
    - In Python we have match case statements that implement switch statements 
- What is a Switch Statement 
    - A switch statement is a control flow statement that executes a block of code among many other based on the value of a variable or expression. 
        - Switch statements are match statements 
    - We use the `match`, `case`, and `default` keywords to define match case statements in Python 
Example
```python 
match direction:
    case "North":
        return x, y + 1 
    case "South":
        return x, y - 1 
    case "East":
        return x + 1, y 
    case "West":
        return x - 1, y 
    case default:
        raise ValueError('Invalid directio')

```

- `match` is a keyword that marks the start of the match block 
- `North` is a variable, arithmetic expression, a boolean expression, or a python object like a list, tuple, or string
- Only one `case` block is executed in the entire match block for any given value of expression
- The `default` block is always present at the end of the match block
    - If none of the expressions match the code inside the default block is executed 
- When to use Match Statements in Python 
    - Match Case statements can be an efficient alternative to `if elif else` statements 
    - When a variable or expression can take multiple values and we need to perform a different action for each possible value we can use match statements 
    - A match case block can be used for other tasks like structural pattern matching in addition to replacing if else blocks

