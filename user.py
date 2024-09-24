
# Encapsulated User class with Searchable interface implementation
# Key Feature: Class Hierarchy & Encapsulation
# The User class represents a user entity in the system and also implements the search functionality.
# Similar to the Book class, it restricts access to the user details and provides controlled access through methods.
class User:
    def __init__(self, username, user_id, password):
        self.username = username
        self.user_id = user_id
        self.password = password
    
    def get_name(self):         # Getter for user's name (Encapsulation)
        return self.username

    def get_password(self):
        return self.password

    def search(self, keyword):
        return keyword.lower() in self.username.lower()