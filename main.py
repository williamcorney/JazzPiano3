import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget
from PyQt6.QtCore import pyqtSignal, QThread
from practical import Practical  # Import the Practical tab class
from settings import Settings    # Import the Settings tab class
import mido
import os
import pickle

class MidiInputThread(QThread):
    """
    This thread listens for MIDI messages and passes them to the Practical tab's `handle_midi_message` method.
    """
    def __init__(self, practical_tab, input_name):
        super().__init__()
        self.practical_tab = practical_tab
        self.input_name = input_name
        self.running = True  # Flag to control the thread

    def run(self):
        try:
            with mido.open_input(self.input_name, callback=self.practical_tab.handle_midi_message) as inport:
                print(f"MIDI input initialized on {self.input_name}.")
                while self.running:  # Keep running the thread until the flag is False
                    pass  # Keeps the loop running, allowing MIDI messages to be handled
        except Exception as e:
            print(f"Error initializing MIDI input: {e}")

    def stop(self):
        """
        Stops the MIDI input thread gracefully.
        """
        self.running = False
        self.quit()
        self.wait()  # Wait until the thread finishes

class Oralia(QMainWindow):
    # Define the signal for data updates
    data_updated = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.tabs = {}  # Dictionary to hold tabs
        self.tab_widget = QTabWidget(self)  # QTabWidget object
        self.tab_widget.setTabPosition(QTabWidget.TabPosition.West)
        self.setCentralWidget(self.tab_widget)

        # Initialize the shared data
        self._shared_data = self.load_data()  # Load shared data from file

        # Pass self (Oralia instance) to each tab
        self.tabs["Practical"] = Practical(self)  # Practical Tab
        self.tabs["Theory"] = Settings(self)      # Theory Tab
        self.tabs["Settings"] = Settings(self)    # Settings Tab

        self.tab_widget.addTab(self.tabs["Practical"], "Practical")
        self.tab_widget.addTab(self.tabs["Theory"], "Theory")
        self.tab_widget.addTab(self.tabs["Settings"], "Settings")

        # Initialize Mido to listen for MIDI input after the GUI is set up
        self.setup_midi_input()

    def setup_midi_input(self):
        """
        Set up Mido to listen for MIDI messages.
        """
        try:
            print("Available MIDI inputs:")
            for port in mido.get_input_names():
                print(port)
            input_name = mido.get_input_names()[0]  # Choose the first available input port
            print(f"Using MIDI input: {input_name}")
            self.midi_thread = MidiInputThread(self.tabs["Practical"], input_name)
            self.midi_thread.start()
        except Exception as e:
            print(f"Error initializing MIDI input: {e}")

    def closeEvent(self, event):
        """
        Override the close event to ensure that the MIDI input thread is stopped before the application closes.
        """
        if hasattr(self, 'midi_thread') and self.midi_thread.isRunning():
            print("Stopping MIDI input thread...")
            self.midi_thread.stop()  # Stop the MIDI thread
        event.accept()  # Proceed with closing the application

    def load_data(self):
        """
        Load shared data from file (using pickle).
        """
        try:
            with open('shared_data.pkl', 'rb') as file:
                data = pickle.load(file)
            print("Shared data loaded from file")
        except FileNotFoundError:
            data = {}  # Default to an empty dictionary if the file doesn't exist
            print("No existing data file found. Starting with an empty dictionary.")
        return data

    def save_data(self, data):
        """
        Save shared data to file (using pickle).
        """
        with open('shared_data.pkl', 'wb') as file:
            pickle.dump(data, file)
        print("Shared data saved to file")

    @property
    def shared_data(self):
        return self._shared_data

    @shared_data.setter
    def shared_data(self, value):
        self._shared_data = value
        self.data_updated.emit(value)  # Emit the signal when the data is updated
        self.save_data(value)  # Save updated data to the file

app = QApplication([])
window = Oralia()
window.show()

# Start the application event loop
sys.exit(app.exec())
