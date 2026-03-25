'''
## Project 1 — Student Record ⭐

### What to build
A `Student` class that stores a student's name, age, and a list of grades. 
The class should be able to add a new grade, calculate the student's average grade, 
and return a summary string describing the student.
'''
class Student():
    #Use defaults in case we have a null/none value
    def __init__(self, name, age, grades= None):
        self.name = name
        self.age = age
        #How to fix if grades is empty
        self.grades = grades if grades is not None else []
    #Below doesn't add a new grade
    #def add_grade(self):
    #    grade_list = []
    #    grade_list.append(self.grades)
    #   return grade_list
    def add_grade(self,grade):
        self.grades.append(grade)
    
    def average_grade(self):
        #Handle empty grades
        if not self.grades:
            return 0
        self.average = sum(self.grades)/len(self.grades)
        return self.average
    #This below depends on average_grade() being called first. If it doesn't exist then the code will crash 
    #def __str__(self):
    #    return f'{self.name}, is {self.age} years old and average grade is {self.average}'
    def __str__(self):
        return f'{self.name}, is {self.age} years old and average grade is {self.average_grade()}'



student1 = Student("Michael", 15, [85,71,90])
grade_list1 = student1.average_grade()
print(grade_list1)
print(student1)

student2 = Student("Alice", 16, [92, 65, 75])
grade_list2= student2.average_grade()
print(grade_list2)
print(student2)

student3 = Student("Jen", 14, [79, 86, 85])
grade_list3 = student3.average_grade()
print(grade_list3)
print(student3)

student4 = Student("Max", 13)
grade_list4 = student4.average_grade()
print(grade_list4)
print(student4)
'''
### Instructions

1. Define the class with an `__init__` method. Think carefully about what data belongs on each 
individual student — these become your instance variables.
2. Write a method to add a single grade to the student's grade list.
3. Write a method to compute and return the average of all grades. What should it return if no grades 
have been added yet?
4. Write a method that returns a human-readable string like: `"Alice, age 20, average grade: 85.4"`.
5. Create at least two student objects and call each method on them to verify they behave independently.

### What to think about
- Every method here uses `self` — ask yourself why. Could any of them work without it?
    - Self is used to traceback to the instance that is being given to the class. No I don't beleive they could work without self
- What happens if you call the average method on a student with no grades? Handle that edge 
case gracefully.
    - Without grades the class doesn't work.  
- Why is the grade list created inside `__init__` rather than as a class variable?
    - Because grades are an attribute to the student. 

### What NOT to do
- Do not use a class variable to store grades. Think about why this would break things if you
 had multiple students.
'''