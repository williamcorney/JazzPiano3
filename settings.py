from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit
# settings.py

class Settings(QWidget):
    def __init__(self, main_window, shared_data_manager):
        super().__init__(main_window)
        self.main_window = main_window  # Access main window
        self.shared_data_manager = shared_data_manager  # Access shared_data_manager directly
        self.layout = QVBoxLayout(self)

        # Create a label to display the current value of the specified key
        self.testkey_label = QLabel("Current value: ")
        self.layout.addWidget(self.testkey_label)

        # Create a QLineEdit for user to specify the key
        self.key_input = QLineEdit(self)
        self.key_input.setPlaceholderText("Enter a key")
        self.layout.addWidget(self.key_input)

        # Create a QLineEdit for user to specify the value
        self.value_input = QLineEdit(self)
        self.value_input.setPlaceholderText("Enter a value")
        self.layout.addWidget(self.value_input)

        # Create a button to set the value of the specified key
        self.set_button = QPushButton("Set value for key")
        self.set_button.clicked.connect(self.set_value_for_key)
        self.layout.addWidget(self.set_button)

        # Create a button to get the value of the specified key
        self.get_button = QPushButton("Get value for key")
        self.get_button.clicked.connect(self.get_value_for_key)
        self.layout.addWidget(self.get_button)

        # Create a button to delete a key from the dictionary
        self.delete_button = QPushButton("Delete key")
        self.delete_button.clicked.connect(self.delete_key)
        self.layout.addWidget(self.delete_button)

        # Connect the signal to update the label when shared data changes
        self.shared_data_manager.data_updated.connect(self.update_label)  # Listen to data_updated signal

        # Set the layout
        self.setLayout(self.layout)

    def set_value_for_key(self):
        # Get the key and value from the QLineEdits
        key = self.key_input.text()
        value = self.value_input.text()

        if key and value:  # Only set if both key and value are provided
            self.set_value(key, value)

    def get_value_for_key(self):
        # Get the key from the QLineEdit and retrieve the corresponding value
        key = self.key_input.text()
        value = self.get_value(key)

        if value is not None:
            self.testkey_label.setText(f"Current value for '{key}': {value}")
        else:
            self.testkey_label.setText(f"No value found for '{key}'")

    def delete_key(self):
        # Get the key from the QLineEdit and delete it from shared data
        key = self.key_input.text()

        if key in self.shared_data_manager.shared_data:  # Access shared data via shared_data_manager
            del self.shared_data_manager.shared_data[key]  # Delete the key from the dictionary
            self.shared_data_manager.trigger_data_update()  # Trigger update
            self.testkey_label.setText(f"Key '{key}' deleted.")
        else:
            self.testkey_label.setText(f"Key '{key}' not found.")

    def set_value(self, key, value):
        data = self.shared_data_manager.shared_data  # Access shared data via shared_data_manager
        data[key] = value
        self.shared_data_manager.trigger_data_update()  # Trigger update
        self.shared_data_manager.shared_data = data  # This triggers data_updated signal

    def get_value(self, key):
        return self.shared_data_manager.shared_data.get(key)  # Access shared data via shared_data_manager

    def update_label(self, updated_data):
        # Update label when shared data is updated
        key = self.key_input.text()
        value = updated_data.get(key) if key else None
        if value is not None:
            self.testkey_label.setText(f"Current value for '{key}': {value}")
        else:
            self.testkey_label.setText(f"No value found for '{key}'")
