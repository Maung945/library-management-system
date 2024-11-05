import json 
import tkinter as tk
from tkinter import messagebox
from book import Book
from user import User
from transaction import BorrowTransaction, ReturnTransaction
from file_manager import FileManager
import os

class LibraryUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("950x450")

        # Initialize sample users
        self.users = [User("Alice", 1, "11"), User("Bob", 2, "22"), User("Steve", 3, "33")]
        self.borrowed_count = {user.get_name(): 0 for user in self.users}
        self.transaction_history = {user.get_name(): [] for user in self.users}
        self.current_user = "Log in as a user"
        self.borrow_limit = 5
        self.books = self.generate_books()
        self.current_user_borrowed_books = []

        # Create UI components
        self.create_widgets()

        # Populate the book listbox
        self.update_book_listbox()

    def generate_books(self):
        """Generate 100 books with 5 copies each."""
        books = []
        book_titles = [
            "The Great Gatsby", "To Kill a Mockingbird", "1984", "The Catcher in the Rye", "Pride and Prejudice",
            "Moby Dick", "The Hobbit", "War and Peace", "The Odyssey", "Crime and Punishment",
            "The Brothers Karamazov", "Jane Eyre", "Wuthering Heights", "Brave New World", "The Scarlet Letter",
            "A Tale of Two Cities", "Animal Farm", "Les Misérables", "The Divine Comedy", "Don Quixote",
            "Frankenstein", "Dracula", "The Adventures of Huckleberry Finn", "Gulliver's Travels", "Lord of the Flies",
            "Alice's Adventures in Wonderland", "Fahrenheit 451", "The Iliad", "Heart of Darkness", "Ulysses",
            "The Old Man and the Sea", "The Grapes of Wrath", "The Picture of Dorian Gray", "Sense and Sensibility",
            "Emma", "David Copperfield", "Great Expectations", "The Sun Also Rises", "Slaughterhouse-Five",
            "One Hundred Years of Solitude", "The Metamorphosis", "In Search of Lost Time", "Madame Bovary",
            "The Sound and the Fury", "Middlemarch", "Anna Karenina", "The Stranger", "Lolita", "Catch-22",
            "Beloved", "The Kite Runner", "The Book Thief", "Life of Pi", "The Road", "Gone with the Wind",
            "The Name of the Rose", "The Count of Monte Cristo", "The Alchemist", "The Lord of the Rings",
            "Harry Potter and the Sorcerer's Stone", "The Chronicles of Narnia", "A Game of Thrones", "The Shining",
            "The Handmaid's Tale", "The Hunger Games", "Dune", "American Gods", "Good Omens", "The Goldfinch",
            "The Time Traveler's Wife", "The Girl with the Dragon Tattoo", "The Da Vinci Code", "The Wind-Up Bird Chronicle",
            "The Night Circus", "The Help", "Gone Girl", "The Fault in Our Stars", "The Perks of Being a Wallflower",
            "The Maze Runner", "Divergent", "Ender's Game", "Ready Player One", "The Martian", "The Giver",
            "Twilight", "Fifty Shades of Grey", "The Outsiders", "The Lovely Bones", "The Princess Bride",
            "The House on Mango Street", "The Secret Life of Bees", "The Joy Luck Club", "Memoirs of a Geisha",
            "The Hunger Games: Catching Fire", "Mockingjay", "The Lost Symbol", "The Shadow of the Wind",
            "The Girl on the Train", "Big Little Lies", "All the Light We Cannot See"
        ]
        # Sort book titles alphabetically
        book_titles.sort()
        
        for i in range(100):
            books.append(Book(book_titles[i % len(book_titles)], f"Author {i + 1}", f"ISBN{i + 1:012}", 5))
        return books
    
    def create_widgets(self):
        # User and Login/Logout buttons
        self.user_label = tk.Label(self.root, text=f"Current User: {self.current_user}", font=("Helvetica", 10, "bold"))
        self.user_label.grid(row=0, column=0, padx=0, pady=5, sticky="e")  # Right-align the label  

        self.login_button = tk.Button(self.root, text="Login", command=self.show_login_dialog)
        self.login_button.grid(row=0, column=1, padx=0, pady=5, sticky="e")

        self.logout_button = tk.Button(self.root, text="Log Out", command=self.logout, state=tk.NORMAL)
        self.logout_button.grid(row=0, column=2, padx=0, pady=5, sticky="w")

        # Transaction message label
        self.transaction_message_label = tk.Label(self.root, text="", fg="green")
        self.transaction_message_label.grid(row=1, column=0, columnspan=3, padx=10, pady=5)

        # Search Box/User
        self.search_label = tk.Label(self.root, text="Search Book/User:")
        self.search_label.grid(row=2, column=0, padx=1, pady=(5, 0), sticky="e")

        self.search_entry = tk.Entry(self.root, width=30)
        self.search_entry.grid(row=2, column=1, padx=1, pady=(5, 0), sticky="w")

        self.search_button = tk.Button(self.root, text="Search", command=self.search)
        self.search_button.grid(row=3, column=0, columnspan=2, pady=5)

        # Transaction history display
        self.transaction_history_display = tk.Text(self.root, height=10, width=70, state=tk.DISABLED)

        # Book and Borrowed Books listboxes
        self.book_label = tk.Label(self.root, text="Library Book List")
        self.book_label.grid(row=4, column=0, padx=10, pady=(10, 0), sticky="w")  # Adjusted row

        self.book_listbox = tk.Listbox(self.root, height=8, width=50)
        self.book_listbox.grid(row=5, column=0, padx=10, pady=10)  # Adjusted row

        self.borrowed_label = tk.Label(self.root, text="User Book List")
        self.borrowed_label.grid(row=4, column=1, padx=5, pady=(10, 0), sticky="w")  # Adjusted row

        self.borrowed_listbox = tk.Listbox(self.root, height=8, width=50)
        self.borrowed_listbox.grid(row=5, column=1, padx=5, pady=10)  # Adjusted row

        # Borrow and Return buttons
        self.borrow_button = tk.Button(self.root, text="Borrow Book", command=self.borrow_book)
        self.borrow_button.grid(row=6, column=0, padx=10, pady=5)  # Adjusted row

        self.return_button = tk.Button(self.root, text="Return Book", command=self.return_book)
        self.return_button.grid(row=6, column=1, padx=10, pady=5)  # Adjusted row

        # Save and Load buttons
        self.save_button = tk.Button(self.root, text="Save Library Data", command=self.save_data)
        self.save_button.grid(row=7, column=0, padx=10, pady=5)

        self.load_button = tk.Button(self.root, text="Load Library Data", command=self.load_data)
        self.load_button.grid(row=7, column=1, padx=10, pady=5)

    def show_login_dialog(self):
        login_window = tk.Toplevel(self.root)
        login_window.title("Login")
        login_window.geometry("300x200")

        tk.Label(login_window, text="Username:").grid(row=0, column=0, padx=10, pady=10)
        username_entry = tk.Entry(login_window)
        username_entry.grid(row=0, column=1)

        tk.Label(login_window, text="Password:").grid(row=1, column=0, padx=10, pady=10)
        password_entry = tk.Entry(login_window, show="*")
        password_entry.grid(row=1, column=1)

        def login():
            username = username_entry.get()
            password = password_entry.get()
            for user in self.users:
                if user.get_name() == username and user.get_password() == password:
                    self.current_user = user
                    self.user_label.config(text=f"Current User: {self.current_user.get_name()}")
                    self.login_button.config(state=tk.DISABLED)
                    self.logout_button.config(state=tk.NORMAL)
                    self.transaction_message_label.config(text="")

                    # Load the borrowed books from the file
                    self.load_borrowed_books(self.current_user.get_name())
                    
                    self.update_transaction_history()
                    login_window.destroy()
                    return
            messagebox.showerror("Login Failed", "Invalid username or password.")

        tk.Button(login_window, text="Login", command=login).grid(row=2, columnspan=2, pady=10)
    
    def save_borrowed_books(self, username):
        # Save borrowed books for the user
        with open(f"{username}_borrowed_books.json", 'w') as f:
            json.dump([book.get_title() for book in self.current_user_borrowed_books], f)

    def load_borrowed_books(self, username):
        # Load borrowed books for the user
        try:
            with open(f"{username}_borrowed_books.json", 'r') as f:
                borrowed_titles = json.load(f)
                for title in borrowed_titles:
                    for book in self.books:
                        if book.get_title() == title:
                            self.current_user_borrowed_books.append(book)
                            break
            self.update_borrowed_listbox()  # Update the borrowed listbox after loading
        except FileNotFoundError:
            pass  # If the file does not exist, simply do nothing

    def logout(self):
        if isinstance(self.current_user, User):
            # Save the borrowed books to a file
            self.save_borrowed_books(self.current_user.get_name())

            self.borrowed_count[self.current_user.get_name()] = 0
            self.current_user_borrowed_books = []

        self.current_user = "Log in as a user"
        self.user_label.config(text=f"Current User: {self.current_user}")
        self.login_button.config(state=tk.NORMAL)
        self.logout_button.config(state=tk.DISABLED)
        
        # Clear the borrowed list and transaction history display
        self.update_borrowed_listbox()  # This will clear the borrowed listbox
        self.borrowed_listbox.delete(0, tk.END)  # Clear User Book List on logout
        self.transaction_history_display.config(state=tk.NORMAL)
        self.transaction_history_display.delete(1.0, tk.END)  # Clear transaction history
        self.transaction_history_display.config(state=tk.DISABLED)

    def borrow_book(self):
        # Check if a user is logged in
        if isinstance(self.current_user, User):
            selected_index = self.book_listbox.curselection()
            if selected_index:
                selected_book = self.books[selected_index[0]]
                if self.borrowed_count[self.current_user.get_name()] >= self.borrow_limit:
                    messagebox.showerror("Limit Reached", f"You can only borrow up to {self.borrow_limit} books.")
                    return

                # Check if the book is available
                if selected_book.get_copies_available() > 0:
                    transaction = BorrowTransaction(selected_book, self.current_user)
                    transaction.execute()
                    self.borrowed_count[self.current_user.get_name()] += 1
                    self.current_user_borrowed_books.append(selected_book)

                    message = f"{self.current_user.get_name()} borrowed '{selected_book.get_title()}'"
                    self.transaction_history[self.current_user.get_name()].append(message)
                    self.transaction_message_label.config(text=message, fg="red")
                    self.update_transaction_history()
                    self.update_book_listbox()
                    self.update_borrowed_listbox()
                else:
                    messagebox.showerror("Book Unavailable", f"The book '{selected_book.get_title()}' is not available.")
        else:
            messagebox.showerror("User Not Logged In", "Please log in as a user to borrow a book.")

    def return_book(self):
        selected_index = self.borrowed_listbox.curselection()
        if selected_index:
            selected_book = self.current_user_borrowed_books[selected_index[0]]
            transaction = ReturnTransaction(selected_book, self.current_user)
            transaction.execute()
            self.borrowed_count[self.current_user.get_name()] -= 1
            self.current_user_borrowed_books.remove(selected_book)
            
            # Update the message in the transaction message label
            message = f"{self.current_user.get_name()} returned '{selected_book.get_title()}'"
            self.transaction_history[self.current_user.get_name()].append(message)
            self.transaction_message_label.config(text=message, fg="green")
            
            self.update_borrowed_listbox()
            self.update_book_listbox()
    
    def search(self):
        keyword = self.search_entry.get()
        results = []
        for book in self.books:
            if book.search(keyword):
                available_text = f"Available: {book.get_copies_available()}"
                results.append(f"Book: {book.get_title()} by {book.get_author()} - {available_text}")

        for user in self.users:
            if user.search(keyword):
                results.append(f"User: {user.get_name()}")

        if results:
            messagebox.showinfo("Search Results", "\n".join(results))
        else:
            messagebox.showinfo("Search Results", "No results found.")

        # Clear the search entry box
        self.search_entry.delete(0, tk.END)

    def save_data(self):
        try:
            data = {
                "books": [
                    {
                        "title": book.get_title(),
                        "author": book.get_author(),
                        "copies_available": book.get_copies_available()
                    } for book in self.books
                ],
                "users": [
                    {
                        "username": user.get_name(),
                        "user_id": user.user_id,
                        "password": user.get_password()
                    } for user in self.users
                ]
            }
            FileManager.save_data(data, "library_data.json")
            messagebox.showinfo("Save Data", "Library data saved successfully!")
        except Exception as e:
            messagebox.showerror("Save Error", f"An error occurred: {e}")


    def load_data(self):
        try:
            data = FileManager.load_data("library_data.json")
            self.books = [Book(book["title"], book["author"], "", book["copies_available"]) for book in data["books"]]
            self.users = [User(user["username"], user["user_id"], user["password"]) for user in data["users"]]
            self.update_book_listbox()
            messagebox.showinfo("Load Data", "Library data loaded successfully!")
        except Exception as e:
            messagebox.showerror("Load Error", f"An error occurred: {e}")

    
    def update_book_listbox(self):
        self.book_listbox.delete(0, tk.END)
        sorted_books = sorted(self.books, key=lambda book: book.get_title()) # Sort books alphabetically by title
        for book in sorted_books:
            available_text = f"Available: {book.get_copies_available()}"
            self.book_listbox.insert(tk.END, f"{book.get_title()} by {book.get_author()} - {available_text}")

    def update_borrowed_listbox(self):
        self.borrowed_listbox.delete(0, tk.END)
        for book in self.current_user_borrowed_books:
            self.borrowed_listbox.insert(tk.END, f"{book.get_title()} by {book.get_author()}")

    def update_transaction_history(self):
        self.transaction_history_display.config(state=tk.NORMAL)
        self.transaction_history_display.delete(1.0, tk.END)
        for message in self.transaction_history[self.current_user.get_name()]:
            self.transaction_history_display.insert(tk.END, message + "\n")
        self.transaction_history_display.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryUI(root)
    root.mainloop()
