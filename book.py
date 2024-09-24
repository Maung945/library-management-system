# Encapsulated Book class with Searchable interface implementation
# Key Feature: Class Hierarchy & Encapsulation
# The Book class represents a single book entity in the system. It uses encapsulation to protect its attributes 
# like title, author, and availability, and only allows access through well-defined getter methods.
class Book:
    def __init__(self, title, author, isbn, copies_available):
        # Private attributes: title, author, ISBN, and copies_available.
        # Encapsulation ensures these fields cannot be directly accessed or modified from outside the class.
        self.__title = title
        self.__author = author
        self.__isbn = isbn
        self.__copies_available = copies_available

    def increment_copies(self):
        self.__copies_available += 1

    def get_copies_available(self):
        return self.__copies_available

    # Getter for book title (Encapsulation)
    def get_title(self):
        return self.__title

    # Getter for book author (Encapsulation)
    def get_author(self):
        return self.__author

    # Getter for copies available (Encapsulation)
    def get_copies_available(self):
        return self.__copies_available
    
    # Borrow a book if available, else raise an exception (Encapsulation + Exception Handling)
    def borrow_book(self):
        if self.__copies_available > 0:
            self.__copies_available -= 1
        else:
            raise Exception("Book is unavailable")

    # Return a book (Encapsulation)
    def return_book(self):
        self.__copies_available += 1

    # Search function to search for a keyword in the title or author (Implements Interface)
    # The search method allows polymorphic behavior when implemented in multiple classes like Book and User.
    def search(self, keyword):
        if keyword in self.__title or keyword in self.__author:
            return True
        return False
