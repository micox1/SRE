# Tuples 
- Just like lists, tuples can hold a swquence of items and have a few key advantages:
    - Tuples are more memory efficient than lists 
    - Tuples have a slightly higher time efficiency  than lists 
- You cannot modify a tuple's elements after creating one and they do not require an extra memory block list lists
    - Tuples are defined with parantheses () with commas to separate 
```python
tuple_example = ('abc', 123, 'def', 456)
```
- Tuples are capable of holding one item as long as the item is followed by a comma
- Tuples and slicing are the same as with lists

# Tuple Built In Functions
- `max()` returns the tuple's maximum value. This function requires all of the values to be of the same data type 
    - If used with strings the function returns the value at the tuple's maximum index as if it was sorted alphabetically. The string closer to the letter Z in the alphabet would have a higher index 
```python
my_tuple = (65, 2, 77)
max(my_tuple)
# Returns 77
```

- `min()` is the opposite of `max()`

- `.index()` takes in a vlue as the argument to find its index in the tuple 
```python 
my_tuple = ('abc', 234, 567, 'def')
my_tuple.index('abc')  # Returns 0
my_tuple.index(567)    # Returns 2
```

- `.count()` takes in a vlue as the argument to find the number of occurrences in the tuple
```python 
my_tuple = ('abc', 'abc', 2, 3, 4)
my_tuple.count('abc')  # returns 2
my_tuple.count(3)      # returns 1
```
