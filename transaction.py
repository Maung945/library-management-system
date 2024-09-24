# Transaction abstract base class
# Key Feature: Polymorphism & Abstract Class
# The Transaction class serves as an abstract base class, providing a common interface for all transaction types.
# This allows dynamic transaction processing via polymorphism.
class Transaction:
    def execute(self):
        # Abstract method to be implemented in derived classes
        pass

# Concrete BorrowTransaction class
# Key Feature: Polymorphism & Encapsulation
# The BorrowTransaction class extends Transaction, allowing dynamic borrowing operations.
class BorrowTransaction(Transaction):
    def __init__(self, book, user):
        # Associated book and user objects
        self.book = book
        self.user = user

    # Executes the borrowing transaction (Polymorphism + Exception Handling)
    def execute(self):
        try:
            self.book.borrow_book()  # Borrow a book, check availability via encapsulation
            print(f"{self.user.get_name()} borrowed {self.book.get_title()}")
        except Exception as e:
            print(e)

# Concrete ReturnTransaction class
# Key Feature: Polymorphism & Encapsulation
# The ReturnTransaction class allows the returning of books, implementing the execute method from Transaction.
class ReturnTransaction(Transaction):
    def __init__(self, book, user):
        # Associated book and user objects
        self.book = book
        self.user = user

    # Executes the return transaction (Polymorphism)
    def execute(self):
        self.book.return_book()  # Return the book, modifies availability via encapsulation
        print(f"{self.user.get_name()} returned {self.book.get_title()}")
