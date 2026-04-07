'''
def __init__(self, title, author, year, available= True):
    Using __init__ is where you would attach attributes to the class 
@staticmethod def is_valid_year(year):
    Why is this a static method? And what is this doing?
        It is static because it isn't about the class or self which is the instance it simply whats to make sure something within the class is true or false
def __repr__(self)
    This allows you to print out readable content when you use print on an instance from the class if not there you would basically get where the object is in memory 
'''
class Book:
    def __init__(self, title, author, year, available= True):
        self.title = title
        self.author = author
        self.year = year
        self.available = available 

    @staticmethod
    def is_valid_year(year):
        if year > 0:
            return True 
        else:
            return False
    
    def __repr__(self):
        return f'{self.title}, {self.author}, {self.year}'

'''
def __init__(self):
    #Again we are making the blueprint of the class 
    #Here you want to truly think about what data is going to be going into the Class. A book would need authors, titles, etc. A library would just need a list of books. Think about this for other 
    instances as well. Cars would be make, model,engine, etc. Make sure that is your thought process when using __init__
self.books = []
    #The function of this class is to hold books fromm our Book class
        def add_book(self, book):

if book.is_valid_year(book.year) == True:
    self.books.append(book)
    #So we gave our add_book method a rule that if it has a valid year to append it to the self.books list 

def find_by_author(self, author):
    results = []
        for book in self.books:
            if book.author == author:
                results.append(book.title)
        return results
    #Here we want to be able to find books by a certain author within self.books. So you would have to iterate through self.books and then find books that match that author
    #book should have these attributes  self.title = title, self.author = author, self.year = year, self.available = available. So if book.author equals the author given it should return the books 

def checkout(self, title):
    #here we are trying to make sure books can be checked out. Again we need to iterate over the books we have and if the title is within the one given mark it as checked out
    for book in self.books:
            if book.title == title:
                book.available= False 
    #the for loop would need to iterate over our list of self.books and find the authors that match
    #remember not to use self.* within the for loop block of code because self here would refer to the Library class and not the book in self.books




'''

class Library:

    def __init__(self):
        self.books = []
    def add_book(self, book):
        if book.is_valid_year(book.year) == True:
            self.books.append(book)
    def find_by_author(self, author):
        results = []
        for book in self.books:
            if book.author == author:
                results.append(book.title)
        return results
    
    def checkout(self, title):
        for book in self.books:
            if book.title == title:
                book.available= False 
    def return_book(self, title): 
        for book in self.books:
            if book.title == title:
                book.available= True 
    @classmethod
    #book_data is any list that will be externally input into the method when running Library.from_list()
    def from_list(cls, book_data):
        new_data = cls()
        for books in book_data:
            title = books["title"]
            author = books["author"]
            year = books["year"]
            #Adding to Book Class
            b = Book(title,author,year)
            #Adding to Library
            new_data.add_book(b)
        return new_data

'''
Write a `@classmethod` on `Library` called `from_list(cls, book_data)` that takes a list of dictionaries (each with title, author, year) and returns a fully populated `Library` instance.     
    new_data = cls()
        This step is creating an empty list meaning, what you currently have inside our __init__ method with self.books would be empty 
    for books in book_data 
        Now the objective of this part of the code is to take data in the form of a dicionary and change it to the correct form for the Library
        So we will iterate through the data that was given using the for loop 
    title = books["title"], author = books["author"], year = books["year"]
        Here we are parsing through the data and assigning it correct values 
    b = Book(title,author,year)
        Now comes the part where we are converting it into a book for our library 
        The Book Class now takes the title, the auther, and the year that was just parsed and makes it into a Book Object for our Library
    new_data.add_book(b)
        Now if you go to the top of the library I have an add_book method
            This method checks if the book has a valid year and adds it to self.books or makes it into an instance of library 
        This step is just adding the new data as an instance 
'''

    


'''
my_book = Book("1984", "George Orwell", 1949)
your_book = Book("Animal Farm", "George Orwell", 1945)
library = Library()
library.add_book(my_book)
library.add_book(your_book)
print(library.books)

library.checkout("1984")
    
print(library.find_by_author("George Orwell"))
'''

