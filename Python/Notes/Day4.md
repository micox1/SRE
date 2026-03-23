# Loops and List Comprehension 

## Loops 
- In a loop we perform a process of iteration or repeating tasks
- Python implements two types of iteration 
    - Indefinite iteration where the number of times the loop is executed depends on how many times a condition is met 
    - Definite iteration where the number of times the loop will be executed is defined in advance 

## For Loops 
- Syntax for a `for` loop
```python 
for <variable> in <collection>:
    <action>
```

## For Loops Using Range 
- Syntax
```python 
for temp in range(6):
  print("Learning Loops")
```
This would output "Learning Loops" 6 times 

## While Loops 
 
- A `while` loop performs a set of instructions as long as a given condition is true 
- Syntax 
```python 
while <conditional statement>: 
  <action>
```
- Example 
```python 
count = 0 
while count <= 3:
  print(count)
  count += 1 
```

- While loops with lists 
	- While loops require some form of a variable to track the condition of the loop to start and stop. Lists have a predetermined length. If we use the length of the lists as the basis for how long our while loop needs to run we can iterate the exact length of the list. We can use the len() function to accomplish this 

```python 
length = len(ingredients)
index = 0 
while index < length:
  print(ingredients[index])
  index += 1
```

## Loop Control 
- You can stop iteration from inside a loop by using the `break` loop control statement. When the program hits a `break` statement it immediately terminates a loop 

- `continue` skips anything that matches the if statement. So the if condition says: "Skip these cases", not "print these cases". If it skips them it does not do the action afterwards. `continue` control statements are usually paired with some form of a conditional like if/elif/else statment. 



