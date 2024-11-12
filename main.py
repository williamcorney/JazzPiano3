from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget
from shared_data_manager import SharedDataManager
from practical import Practical  # Import the Practical tab class
from settings import Settings    # Import the Settings tab class
from midi_handler import MidiHandler
import sys
class Oralia(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tabs = {}
        self.tab_widget = QTabWidget(self)
        self.tab_widget.setTabPosition(QTabWidget.TabPosition.West)
        self.setCentralWidget(self.tab_widget)

        # Initialize SharedDataManager
        self.shared_data_manager = SharedDataManager()

        # Load shared data via SharedDataManager
        self._shared_data = self.shared_data_manager.load_data()

        # Initialize tabs after setting up shared data manager
        self.tabs["Practical"] = Practical(self)
        self.tabs["Theory"] = Settings(self)
        self.tabs["Settings"] = Settings(self)

        # Add tabs to the tab widget
        self.tab_widget.addTab(self.tabs["Practical"], "Practical")
        self.tab_widget.addTab(self.tabs["Theory"], "Theory")
        self.tab_widget.addTab(self.tabs["Settings"], "Settings")

        # Initialize MIDI handler after tabs are created
        self.midi_handler = MidiHandler(self.tabs["Practical"])
        self.midi_handler.setup_midi_input()

    # Now you can safely remove the `closeEvent` method
    # The MIDI cleanup will be handled by MidiHandler

app = QApplication([])
window = Oralia()
window.show()

# Start the application event loop
sys.exit(app.exec())
