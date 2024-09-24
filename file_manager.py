
import json

# FileManager for data persistence
# Key Feature: Data Persistence
# The FileManager class handles saving and loading data from a JSON file, allowing the system to persist data.
class FileManager:
    
    @staticmethod
    def save_data(data, filename):
        # Saves data to a JSON file for persistence
        with open(filename, 'w') as file:
            json.dump(data, file)

    @staticmethod
    def load_data(filename):
        # Loads data from a JSON file
        with open(filename, 'r') as file:
            return json.load(file)

