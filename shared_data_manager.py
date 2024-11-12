# shared_data_manager.py
from PyQt6.QtCore import QObject, pyqtSignal
import pickle

class SharedDataManager(QObject):
    data_updated = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self._shared_data = {}

    def load_data(self):
        """
        Load shared data from file (using pickle).
        """
        try:
            with open('shared_data.pkl', 'rb') as file:
                self._shared_data = pickle.load(file)
            print("Shared data loaded from file")
        except FileNotFoundError:
            self._shared_data = {}  # Default to an empty dictionary if the file doesn't exist
            print("No existing data file found. Starting with an empty dictionary.")
        return self._shared_data

    def save_data(self, data):
        """
        Save shared data to file (using pickle).
        """
        with open('shared_data.pkl', 'wb') as file:
            pickle.dump(data, file)
        print("Shared data saved to file")
        self.data_updated.emit(data)

    @property
    def shared_data(self):
        return self._shared_data

    @shared_data.setter
    def shared_data(self, value):
        self._shared_data = value
        self.save_data(value)  # Save updated data
        self.data_updated.emit(value)  # Emit the signal when data is updated
