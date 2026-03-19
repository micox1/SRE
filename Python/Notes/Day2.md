#  Lists
- What is a list
    - It is a built in data structure that allows us to work with a collection of data in sequential order 

Example of a List 
```python 
heights = [51, 44, 80, 69]
```

- `.append()` allows us to add an element to the end of the list 
```python
append_example_list.append("item")
```

- `.remove()` allows you to delete an element from a list 
```python 
append_example_list.remove("item")
```

- You can also add to a list using `+`:
```python 
my_list = [1,2,3,4]
new_list = my_list + [5]
```

- Indexing a list 
```python
pancake_recipe = ["eggs", "flour", "butter", "milk", "sugar", "love"]
print(pancake_recipe[-1])
# Would print: love`
```

- What are 2D Lists?
    - They are a list inside a list 
```python
heights = [['Noelle', 61], ['Ava', 70], ['Sam', 67]]
```
- Accessing 2D Lists 
```python 
# Access the sublist at index 0, and then access the 1st index of that sublist.
noelles_height = heights[0][1]
print(noelles_height)  # would output 61
```

- Working with Lists
    - `.count()` is to count the number of occurennces of an element in a list 
    - `.insert()` is a list method to insert an element into a specific index of a list
    - `.pop()` allows you to remove an element from a specific index or from the end of a list 
    - `.range()` creates a sequence of integers
    - `.len()` gets you the length of a list 
    - `.sort()` sorts the list 

## Slicing Lists
```python 
letters = ["a", "b", "c", "d", "e", "f", "g"]
# Suppose we want to select from "b" through "f".
# letters[start:end]
# start is the index of the first element we want to include
# end is the index of one MORE than the last element we want

sliced_list = letters[1:6]
print(sliced_list)
# Would output: ["b", "c", "d", "e", "f"]
```

## Combining Lists: Zip Function 
- The `zip` function allows us to quickly combine associated data sets without needing to rely on multi-dimensional lists
```python 
names = ["Jenny", "Alexus", "Sam", "Grace"]
heights = [61, 70, 67, 64]
names_and_heights = zip(names, heights)
# Would output: <zip object at 0x7f1631e86b48>

converted_list = list(names_and_heights)
print(converted_list)
# Outputs: [('Jenny', 61), ('Alexus', 70), ('Sam', 67), ('Grace', 64)]
```

- Notice the inner lists don't use square brackes around the values. This is because they have been converted into tuples


