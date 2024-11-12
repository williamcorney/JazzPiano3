from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QListWidget, \
    QGraphicsScene, QGraphicsView, QGraphicsPixmapItem, QAbstractItemView
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QPixmap, QFont
from note_handler import note_handler  # Importing the note_handler function
import pickle

class Practical(QWidget):
    # Define custom signals for note on/off
    note_on_signal = pyqtSignal(int, str)
    note_off_signal = pyqtSignal(int)

    def __init__(self, parent=None, shared_data_manager=None):
        super().__init__(parent)
        self.shared_data_manager = shared_data_manager  # Store the shared data manager instance
        self.pixmap_item = {}

        # Load theory from pickle file
        self.load_theory()

        # Setup the GUI
        self.setup_layout()
        self.setup_theory_lists()
        self.setup_piano_keys_view()
        self.setup_labels()
        self.setup_go_button()

        # Connect signals to methods
        self.connect_signals()

    def load_theory(self):
        """Load theory from pickle file"""
        try:
            with open('theory.pkl', 'rb') as file:
                self.Theory = pickle.load(file)
            print("Theory loaded from file")
        except FileNotFoundError:
            self.Theory = {}  # Default empty dictionary if file is not found
            print("Theory file not found. Using default.")

    def setup_layout(self):
        """Setup the main layout for the Practical tab"""
        self.layout = QVBoxLayout(self)
        self.label = QLabel("This is the Practical tab.")
        self.layout.addWidget(self.label)

        self.horizontal = QHBoxLayout()
        self.layout.addLayout(self.horizontal)

    def setup_theory_lists(self):
        """Setup the theory list widgets and populate them"""
        self.theory1, self.theory2, self.theory3 = QListWidget(), QListWidget(), QListWidget()
        for theory in [self.theory1, self.theory2, self.theory3]:
            self.horizontal.addWidget(theory, stretch=1)

        self.theory1.addItems(["Notes", "Scales", "Triads", "Sevenths", "Modes", "Shells"])
        self.theory2.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)

    def setup_piano_keys_view(self):
        """Setup the QGraphicsView for piano keys"""
        self.Scene = QGraphicsScene()
        self.BackgroundPixmap = QPixmap(
            "/Users/williamcorney/PycharmProjects/JazzPiano2/Practical/Images/Piano/keys.png")
        self.BackgroundItem = QGraphicsPixmapItem(self.BackgroundPixmap)
        self.Scene.addItem(self.BackgroundItem)

        self.View = QGraphicsView(self.Scene)
        self.View.setFixedSize(self.BackgroundPixmap.size())
        self.View.setSceneRect(0, 0, self.BackgroundPixmap.width(), self.BackgroundPixmap.height())
        self.View.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.View.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.layout.addWidget(self.View)

    def setup_labels(self):
        """Setup the labels on the GUI"""
        self.horizontal_vertical = QVBoxLayout()
        self.horizontal.addLayout(self.horizontal_vertical, 2)

        # Create the labels with relevant text
        self.labels = {}
        for key, text in [('key_label', 'Key: C Major'),
                          ('inversion_label', 'Inversion: Root'),
                          ('fingering_label', 'Fingering: 1-2-3-4-5'),
                          ('score_value', 'Score: 100')]:
            label = QLabel(text)
            if key == 'key_label':
                label.setFont(QFont("Arial", 32))  # Set the font for 'key_label'
            self.labels[key] = label
            self.horizontal_vertical.addWidget(label)

    def setup_go_button(self):
        """Setup the 'Go' button"""
        self.go_button = QPushButton("Go")
        self.go_button.clicked.connect(self.go_button_clicked)
        self.horizontal_vertical.addWidget(self.go_button)

    def connect_signals(self):
        """Connect the signals to their respective handlers"""
        self.note_on_signal.connect(self.insert_note)
        self.note_off_signal.connect(self.delete_note)

        # Connect the theory list widgets to their respective methods
        self.theory1.itemClicked.connect(self.theory1_clicked)
        self.theory2.itemClicked.connect(self.theory2_clicked)
        self.theory3.itemClicked.connect(self.theory3_clicked)

    def theory1_clicked(self):
        self.labels['score_value'].setText("")
        self.labels['fingering_label'].clear()
        self.labels['key_label'].setText("")

        self.theory2.clear()
        self.theory3.clear()
        self.theorymode = self.theory1.selectedItems()[0].text()

        theory_items = {
            "Notes": ["Naturals", "Sharps", "Flats"],
            "Scales": ["Major", "Minor", "Harmonic Minor", "Melodic Minor"],
            "Triads": ["Major", "Minor"],
            "Sevenths": ["Maj7", "Min7", "7", "Dim7", "m7f5"],
            "Modes": ["Ionian", "Dorian", "Phrygian", "Lydian", "Mixolydian", "Aeolian", "Locrian"],
            "Shells": ["Major", "Minor", "Dominant"]
        }

        if self.theorymode in theory_items:
            self.theory2.addItems(theory_items[self.theorymode])

    def theory2_clicked(self):
        self.theory3.clear()
        self.theory2list = [item.text() for item in self.theory2.selectedItems()]

        theory3_items = {
            "Notes": [],
            "Scales": ["Right", "Left"],
            "Triads": ["Root", "First", "Second"],
            "Sevenths": ["Root", "First", "Second", "Third"],
            "Modes": [],
            "Shells": ["3/7", "7/3"]
        }

        if self.theorymode in theory3_items:
            self.theory3.addItems(theory3_items[self.theorymode])

    def theory3_clicked(self):
        modes_requiring_list = {"Notes", "Scales", "Triads", "Sevenths", "Shells"}
        if self.theorymode in modes_requiring_list:
            self.theory3list = [item.text() for item in self.theory3.selectedItems()]

    def insert_note(self, note, color):
        """
        Insert a note (visual representation) on the piano keyboard at the given position.
        """
        self.xcord = self.Theory["NoteCoordinates"][note % 12] + ((note // 12) - 4) * 239
        self.pixmap_item[note] = QGraphicsPixmapItem(
            QPixmap("/Users/williamcorney/PycharmProjects/JazzPiano2/Practical/Images/Piano/key_" + color + self.Theory["NoteFilenames"][note % 12]))
        self.pixmap_item[note].setPos(self.xcord, 0)
        current_scene = self.pixmap_item[note].scene()
        if current_scene:
            current_scene.removeItem(self.pixmap_item[note])
        self.Scene.addItem(self.pixmap_item[note])

    def delete_note(self, note):
        if note in self.pixmap_item:
            if self.pixmap_item[note].scene():
                self.pixmap_item[note].scene().removeItem(self.pixmap_item[note])
            del self.pixmap_item[note]

    def handle_midi_message(self, message):
        note_handler(self, message)  # Pass self (Practical instance) and the MIDI message

    def go_button_clicked(self):
        """Handle 'Go' button click event"""
        print("Go button clicked")

        # Example: Save some data to shared_data_manager when the button is clicked
        self.shared_data_manager.shared_data["example_key"] = "example_value"
        self.shared_data_manager.save_data(self.shared_data_manager.shared_data)
