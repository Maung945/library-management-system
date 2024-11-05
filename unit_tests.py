import unittest
from book import Book
from transaction import BorrowTransaction, ReturnTransaction
from user import User
from file_manager import FileManager
import json
import os

class TestLibrarySystem(unittest.TestCase):

    def setUp(self):
        # Sample book and user data for testing
        self.book = Book("Test Book", "Author Test", "1234567890123", 3)
        self.user = User("TestUser", 1, "password123")

    def test_book_initialization(self):
        """Test initializing a Book object with title, author, ISBN, and copies available."""
        self.assertEqual(self.book.get_title(), "Test Book")
        self.assertEqual(self.book.get_author(), "Author Test")
        self.assertEqual(self.book.get_copies_available(), 3)
        print("Book initialization test passed: Title, author, and available copies match initialization values.")

    def test_book_borrowing(self):
        """Test borrowing a book decreases available copies by 1."""
        self.book.borrow_book()
        self.assertEqual(self.book.get_copies_available(), 2)
        print("Book borrowing test passed: Available copies decreased by 1 after borrowing.")

    def test_borrow_book_exception(self):
        """Test borrowing a book raises an exception when no copies are available."""
        self.book.borrow_book()
        self.book.borrow_book()
        self.book.borrow_book()  # All copies should be borrowed
        with self.assertRaises(Exception) as context:
            self.book.borrow_book()
        self.assertEqual(str(context.exception), "Book is unavailable")
        print("Borrowing unavailable book test passed: Exception raised correctly when no copies available.")

    def test_return_book(self):
        """Test returning a book increases available copies by 1."""
        self.book.borrow_book()
        self.book.return_book()
        self.assertEqual(self.book.get_copies_available(), 3)
        print("Book return test passed: Available copies increased by 1 after returning.")

    def test_file_manager_save_load(self):
        """Test FileManager's save_data and load_data methods."""
        data = {"name": "Test User", "id": 1}
        filename = "test_file.json"
        FileManager.save_data(data, filename)
        loaded_data = FileManager.load_data(filename)
        self.assertEqual(data, loaded_data)
        print("FileManager save/load test passed: Data loaded matches data saved.")
        
        os.remove(filename)             # Clean up test file

    def test_user_search(self):
        """Test the search functionality of the User class for a keyword in the username."""
        self.assertTrue(self.user.search("testuser"))
        self.assertFalse(self.user.search("nonexistent"))
        print("User search test passed: User found with correct keyword and not found with unrelated keyword.")

if __name__ == "__main__":   # Run tests with additional output for each test
    
    suite = unittest.TestLoader().loadTestsFromTestCase(TestLibrarySystem)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
